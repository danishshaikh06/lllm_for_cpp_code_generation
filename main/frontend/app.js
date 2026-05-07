const promptEl = document.getElementById("prompt");
const maxTokensEl = document.getElementById("maxTokens");
const temperatureEl = document.getElementById("temperature");
const topKEl = document.getElementById("topK");
const modelInfoEl = document.getElementById("modelInfo");
const statusEl = document.getElementById("status");
const responseEl = document.getElementById("response");
const generateButton = document.getElementById("generateButton");
const copyButton = document.getElementById("copyButton");

async function loadModelInfo() {
  try {
    const response = await fetch("/api/model-info");
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Unable to load model info.");
    }

    if (!payload.using_finetuned_model) {
      modelInfoEl.textContent = "Active model: base checkpoint. Fine-tuned checkpoint not found yet.";
      return;
    }

    const quality = payload.quality_snapshot;
    const qualityText = quality
      ? `Latest validation perplexity: ${quality.value} (${quality.notes})`
      : "No quality snapshot available.";

    modelInfoEl.textContent = `Active model: fine-tuned checkpoint. ${qualityText}`;
  } catch (error) {
    modelInfoEl.textContent = `Model info unavailable: ${error.message}`;
  }
}

async function generateResponse() {
  const prompt = promptEl.value.trim();
  if (!prompt) {
    statusEl.textContent = "Enter a prompt before generating.";
    return;
  }

  generateButton.disabled = true;
  statusEl.textContent = "Generating response from your local model...";
  responseEl.textContent = "Working...";

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        max_new_tokens: Number(maxTokensEl.value),
        temperature: Number(temperatureEl.value),
        top_k: Number(topKEl.value),
      }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Request failed.");
    }

    responseEl.textContent = payload.response || "The model returned an empty response.";
    statusEl.textContent = "Generation complete.";
  } catch (error) {
    responseEl.textContent = "";
    statusEl.textContent = error.message;
  } finally {
    generateButton.disabled = false;
  }
}

async function copyResponse() {
  const text = responseEl.textContent.trim();
  if (!text || text === "Your model output will appear here.") {
    statusEl.textContent = "Generate something first, then copy it.";
    return;
  }

  await navigator.clipboard.writeText(text);
  statusEl.textContent = "Response copied to clipboard.";
}

generateButton.addEventListener("click", generateResponse);
copyButton.addEventListener("click", copyResponse);
loadModelInfo();
