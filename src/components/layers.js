export function renderLayers(container, layers) {
  container.innerHTML = layers
    .map(
      (layer) => `
      <article class="layer">
        <div>
          <h3>${layer.title}</h3>
          <p class="summary">${layer.summary}</p>
        </div>
        <div class="tags">
          ${layer.tags.map((tag) => `<span class="tag">${tag}</span>`).join('')}
        </div>
      </article>
    `
    )
    .join('');
}
