const UPSTREAM_ORIGIN = 'https://assets.drthorne.uk';
const ALLOWED_ASSETS = new Set([
  'model.glb',
  'build-result.json',
  'front.png',
  'three-quarter.png',
]);

function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'Referrer-Policy': 'no-referrer',
      'X-Content-Type-Options': 'nosniff',
    },
  });
}

function normalizedPath(value) {
  if (Array.isArray(value)) return value.join('/');
  return value || '';
}

function allowed(path, method) {
  const parts = path.split('/').filter(Boolean);
  if (parts[0] === 'v1' && parts[1] === 'builds') {
    if (parts.length === 2) return method === 'GET';
    if (parts.length === 3) return method === 'GET';
    if (parts.length === 4 && parts[3] === 'viewer-session') return method === 'POST';
    if (parts.length === 4 && parts[3] === 'delete') return method === 'POST';
    return false;
  }

  if (parts[0] === 's' && parts.length === 3) {
    return method === 'GET' && parts[1].length >= 40 && ALLOWED_ASSETS.has(parts[2]);
  }

  return false;
}

function copyResponseHeaders(upstream) {
  const headers = new Headers();
  for (const name of [
    'content-type',
    'content-length',
    'cache-control',
    'content-disposition',
    'referrer-policy',
    'x-content-type-options',
  ]) {
    const value = upstream.headers.get(name);
    if (value) headers.set(name, value);
  }
  headers.set('Cache-Control', 'private, no-store');
  headers.set('Referrer-Policy', 'no-referrer');
  headers.set('X-Content-Type-Options', 'nosniff');
  return headers;
}

export async function onRequest(context) {
  const { request, params } = context;
  const accessJwt = request.headers.get('Cf-Access-Jwt-Assertion');

  if (!accessJwt) {
    return json(401, { error: 'access_required' });
  }

  const path = normalizedPath(params.path);
  if (!allowed(path, request.method)) {
    return json(404, { error: 'not_found' });
  }

  const upstreamHeaders = new Headers();
  upstreamHeaders.set('Cf-Access-Token', accessJwt);
  const contentType = request.headers.get('content-type');
  if (contentType) upstreamHeaders.set('Content-Type', contentType);

  let upstream;
  try {
    upstream = await fetch(`${UPSTREAM_ORIGIN}/${path}`, {
      method: request.method,
      headers: upstreamHeaders,
      body: request.method === 'GET' || request.method === 'HEAD' ? undefined : request.body,
      redirect: 'manual',
    });
  } catch {
    return json(502, { error: 'upstream_unreachable' });
  }

  const responseHeaders = copyResponseHeaders(upstream);
  const upstreamType = upstream.headers.get('content-type') || '';

  if (upstreamType.includes('application/json')) {
    const text = await upstream.text();
    if (upstream.ok && path.endsWith('/viewer-session')) {
      try {
        const payload = JSON.parse(text);
        if (typeof payload.viewer_url === 'string') {
          const origin = new URL(request.url).origin;
          payload.viewer_url = payload.viewer_url.replaceAll(
            `${UPSTREAM_ORIGIN}/`,
            `${origin}/api/`,
          );
        }
        return new Response(JSON.stringify(payload), {
          status: upstream.status,
          headers: responseHeaders,
        });
      } catch {
        return json(502, { error: 'invalid_upstream_response' });
      }
    }

    return new Response(text, {
      status: upstream.status,
      headers: responseHeaders,
    });
  }

  return new Response(upstream.body, {
    status: upstream.status,
    headers: responseHeaders,
  });
}
