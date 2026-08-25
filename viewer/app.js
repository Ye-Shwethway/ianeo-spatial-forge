const params = new URLSearchParams(window.location.search);

const model = document.querySelector('#model');
const status = document.querySelector('#status');
const title = document.querySelector('#title');
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

const customTitle = params.get('title');
if (customTitle) title.textContent = customTitle;

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

async function loadMetadata() {
  const metaUrl = explicitUrl('meta');
  if (!metaUrl) return;

  setStatus(modelUrl ? 'Loading details' : 'Loading metadata');

  try {
    const response = await fetch(metaUrl, { credentials: 'omit' });
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

loadMetadata();
