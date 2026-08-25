const params = new URLSearchParams(window.location.search);
const API_ORIGIN = 'https://assets.drthorne.uk';
const API_CONNECTED_KEY = 'spatial-forge-api-connected-v1';

const status = document.querySelector('#status');
const title = document.querySelector('#title');
const librarySection = document.querySelector('#librarySection');
const libraryMessage = document.querySelector('#libraryMessage');
const buildList = document.querySelector('#buildList');
const refreshLibrary = document.querySelector('#refreshLibrary');
const viewerMode = document.querySelector('#viewerMode');

const model = document.querySelector('#model');
const hint = document.querySelector('#modelHint');
const resetButton = document.querySelector('#resetButton');
const downloadModel = document.querySelector('#downloadModel');
const previewSection = document.querySelector('#previewSection');
const frontFigure = document.querySelector('#frontFigure');
const threeQuarterFigure = document.querySelector('#threeQuarterFigure');
const frontPreview = document.querySelector('#frontPreview');
const threeQuarterPreview = document.querySelector('#threeQuarterPreview');
const metadataEmpty = document.querySelector('#metadataEmpty');
const metadata = document.querySelector('#metadata');
const summary = document.querySelector('#summary');
const controls = document.querySelector('#controls');
const unsupportedSection = document.querySelector('#unsupportedSection');
const unsupported = document.querySelector('#unsupported');

function explicitUrl(name) {
  const raw = params.get(name);
  if (!raw) return null;
  try {
    return new URL(raw, window.location.href).href;
  } catch {
    return null;
  }
}

function setStatus(text) {
  status.textContent = text;
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes < 0) return '—';
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? 'Unknown time' : date.toLocaleString();
}

async function apiFetch(path, options = {}) {
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), 12000);
  try {
    const response = await fetch(`${API_ORIGIN}${path}`, {
      credentials: 'include',
      ...options,
      signal: controller.signal,
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('connection timed out');
    throw error;
  } finally {
    window.clearTimeout(timer);
  }
}

function connectPrivateLibrary() {
  setStatus('Connecting');
  refreshLibrary.disabled = true;
  libraryMessage.textContent = 'Connecting private storage…';
  libraryMessage.classList.remove('hidden');
  sessionStorage.setItem(API_CONNECTED_KEY, '1');
  const returnUrl = `${window.location.origin}${window.location.pathname}`;
  window.location.replace(`${API_ORIGIN}/browser-connect?return=${encodeURIComponent(returnUrl)}`);
}

function makeBuildCard(build) {
  const card = document.createElement('article');
  card.className = 'build-card';

  const body = document.createElement('div');
  body.className = 'build-body';

  const heading = document.createElement('h3');
  heading.textContent = build.build_id;

  const meta = document.createElement('div');
  meta.className = 'build-meta';
  const character = build.character_id ? `Character: ${build.character_id}` : 'Character metadata unavailable';
  const version = build.version === undefined || build.version === null ? '' : ` · v${build.version}`;
  meta.textContent = `${character}${version}`;

  const detail = document.createElement('div');
  detail.className = 'build-detail';
  detail.textContent = `${formatBytes(build.size_bytes)} · ${formatDate(build.created_at)}`;

  body.append(heading, meta, detail);

  const actions = document.createElement('div');
  actions.className = 'build-actions';

  const open = document.createElement('button');
  open.type = 'button';
  open.textContent = 'Open 3D';
  open.addEventListener('click', async () => {
    open.disabled = true;
    setStatus('Opening');
    try {
      const session = await apiFetch(`/v1/builds/${encodeURIComponent(build.build_id)}/viewer-session`, {
        method: 'POST',
      });
      window.location.assign(session.viewer_url);
    } catch (error) {
      open.disabled = false;
      setStatus('Open failed');
      libraryMessage.textContent = `Could not open build: ${error.message}`;
      libraryMessage.classList.remove('hidden');
    }
  });

  const remove = document.createElement('button');
  remove.type = 'button';
  remove.className = 'danger-button';
  remove.textContent = 'Delete';
  remove.addEventListener('click', async () => {
    if (!window.confirm(`Delete ${build.build_id} permanently?`)) return;
    remove.disabled = true;
    setStatus('Deleting');
    try {
      await apiFetch(`/v1/builds/${encodeURIComponent(build.build_id)}/delete`, { method: 'POST' });
      await loadLibrary();
    } catch (error) {
      remove.disabled = false;
      setStatus('Delete failed');
      libraryMessage.textContent = `Could not delete build: ${error.message}`;
      libraryMessage.classList.remove('hidden');
    }
  });

  actions.append(open, remove);
  card.append(body, actions);
  return card;
}

async function loadLibrary() {
  setStatus('Loading');
  refreshLibrary.textContent = 'Refresh';
  refreshLibrary.disabled = true;
  libraryMessage.textContent = 'Loading builds…';
  libraryMessage.classList.remove('hidden');
  buildList.replaceChildren();

  try {
    const data = await apiFetch('/v1/builds');
    const builds = Array.isArray(data.builds) ? data.builds : [];
    if (!builds.length) {
      libraryMessage.textContent = 'No private builds yet.';
    } else {
      libraryMessage.classList.add('hidden');
      for (const build of builds) buildList.appendChild(makeBuildCard(build));
    }
    setStatus(`${builds.length} build${builds.length === 1 ? '' : 's'}`);
  } catch (error) {
    sessionStorage.removeItem(API_CONNECTED_KEY);
    libraryMessage.textContent = `Private storage connection failed: ${error.message}`;
    refreshLibrary.textContent = 'Reconnect';
    setStatus('Library failed');
  } finally {
    refreshLibrary.disabled = false;
  }
}

function addSummary(label, value) {
  if (value === undefined || value === null || value === '') return;
  const dt = document.createElement('dt');
  const dd = document.createElement('dd');
  dt.textContent = label;
  dd.textContent = String(value);
  summary.append(dt, dd);
}

function showPreview(url, figure, image) {
  if (!url) return false;
  image.src = url;
  figure.classList.remove('hidden');
  return true;
}

async function loadViewer() {
  librarySection.classList.add('hidden');
  viewerMode.classList.remove('hidden');

  const customTitle = params.get('title');
  title.textContent = customTitle || '3D Viewer';

  const modelUrl = explicitUrl('model');
  if (modelUrl) {
    model.src = modelUrl;
    hint.classList.add('hidden');
    downloadModel.href = modelUrl;
    downloadModel.classList.remove('hidden');
    setStatus('Loading 3D');
    model.addEventListener('load', () => setStatus('3D ready'));
    model.addEventListener('error', () => setStatus('3D failed'));
  }

  resetButton.addEventListener('click', () => {
    model.cameraOrbit = 'auto auto auto';
    model.cameraTarget = 'auto auto auto';
    model.fieldOfView = 'auto';
    model.jumpCameraToGoal();
  });

  const frontUrl = explicitUrl('front');
  const threeQuarterUrl = explicitUrl('threeQuarter');
  if (
    showPreview(frontUrl, frontFigure, frontPreview) |
    showPreview(threeQuarterUrl, threeQuarterFigure, threeQuarterPreview)
  ) {
    previewSection.classList.remove('hidden');
  }

  const metaUrl = explicitUrl('meta');
  if (!metaUrl) return;
  setStatus(modelUrl ? 'Loading details' : 'Loading metadata');

  try {
    const response = await fetch(metaUrl, { credentials: 'include' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();

    metadataEmpty.classList.add('hidden');
    metadata.classList.remove('hidden');
    addSummary('Character', data.character_id);
    addSummary('Version', data.version);
    addSummary('Status', data.status);
    addSummary('Blender', data.runtime?.blender);
    addSummary('MPFB', data.runtime?.mpfb);
    addSummary('GLB meshes', data.structural?.mesh_count);
    addSummary('Skins', data.structural?.skin_count);
    addSummary('Joints', data.structural?.joint_count);

    for (const [name, value] of Object.entries(data.applied_controls ?? {})) {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = `${name} ${value}`;
      controls.appendChild(chip);
    }

    const unsupportedFields = Array.isArray(data.unsupported_fields) ? data.unsupported_fields : [];
    if (unsupportedFields.length) {
      unsupportedSection.classList.remove('hidden');
      for (const item of unsupportedFields) {
        const box = document.createElement('div');
        box.className = 'warning';
        const heading = document.createElement('strong');
        const requested = item.requested_value === undefined
          ? ''
          : ` — requested ${item.requested_value}${item.unit ? ` ${item.unit}` : ''}`;
        heading.textContent = `${item.field ?? 'Unsupported request'}${requested}`;
        const reason = document.createElement('div');
        reason.textContent = item.reason ?? 'No supported mapping was reported.';
        box.append(heading, reason);
        unsupported.appendChild(box);
      }
    }

    if (!modelUrl) setStatus('Metadata ready');
    else if (model.loaded) setStatus('Ready');
  } catch (error) {
    metadataEmpty.textContent = `Could not load build metadata: ${error.message}`;
    setStatus('Metadata failed');
  }
}

const viewerRequested = Boolean(explicitUrl('model') || explicitUrl('meta'));
if (viewerRequested) {
  loadViewer();
} else {
  refreshLibrary.addEventListener('click', () => {
    if (sessionStorage.getItem(API_CONNECTED_KEY) === '1') loadLibrary();
    else connectPrivateLibrary();
  });
  if (sessionStorage.getItem(API_CONNECTED_KEY) === '1') loadLibrary();
  else connectPrivateLibrary();
}
