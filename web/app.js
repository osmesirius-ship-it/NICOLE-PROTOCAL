const apiBase = "http://localhost:8000";

const identityBtn = document.getElementById("btn-identity");
const chunkBtn = document.getElementById("btn-chunk");
const ingestBtn = document.getElementById("btn-ingest");

identityBtn.addEventListener("click", async () => {
  const name = document.getElementById("identity-name").value;
  const role = document.getElementById("identity-role").value;
  const payload = { name, tags: { role } };
  const res = await fetch(`${apiBase}/api/v1/identity`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  document.getElementById("identity-result").textContent = JSON.stringify(
    await res.json(),
    null,
    2
  );
});

chunkBtn.addEventListener("click", async () => {
  const content = document.getElementById("chunk-content").value;
  const metaRaw = document.getElementById("chunk-meta").value;
  const metadata = parseJSON(metaRaw);
  const payload = { content, metadata };
  const res = await fetch(`${apiBase}/api/v1/context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  document.getElementById("chunk-result").textContent = JSON.stringify(
    await res.json(),
    null,
    2
  );
});

ingestBtn.addEventListener("click", async () => {
  const query = document.getElementById("ingest-query").value;
  const targetFormat = document.getElementById("target-format").value;
  const daStyle = document.getElementById("da-style").value;
  const useSymbolic = document.getElementById("symbolic-toggle").checked;

  const config = {
    target_format: targetFormat,
    use_symbolic_overlay: useSymbolic,
    style_prefs: { da_style: daStyle },
  };

  const res = await fetch(`${apiBase}/api/v1/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, config }),
  });
  document.getElementById("ingest-result").textContent = JSON.stringify(
    await res.json(),
    null,
    2
  );
});

function parseJSON(raw) {
  try {
    return JSON.parse(raw);
  } catch (err) {
    return {};
  }
}
