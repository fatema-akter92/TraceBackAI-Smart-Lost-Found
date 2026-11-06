/**
 * Feature 4: AI Image Recognition & Auto-categorization
 */

function setupAiCategoryAssistant() {
    const titleInput = document.getElementById('id_title');
    const descInput = document.getElementById('id_description');
    const imageInput = document.getElementById('id_image');
    const categorySelect = document.getElementById('id_category');
    const badgeContainer = document.getElementById('ai-suggest-badge');

    if (!categorySelect || !badgeContainer) return;

    let debounceTimer = null;

    function checkCategorySuggestion() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const text = `${titleInput ? titleInput.value : ''} ${descInput ? descInput.value : ''}`;
            const filename = (imageInput && imageInput.files.length > 0) ? imageInput.files[0].name : '';

            if (text.trim().length < 3 && !filename) return;

            fetch(`/items/api/ai-category-suggest/?text=${encodeURIComponent(text)}&filename=${encodeURIComponent(filename)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success' && data.category_id) {
                        badgeContainer.classList.remove('hidden');
                        badgeContainer.innerHTML = `
                            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-100 text-cyan-800 text-xs font-semibold shadow-xs">
                                <i class="fas fa-magic text-cyan-600"></i> AI Detected: <strong>${data.category_name}</strong> (${data.confidence}% confidence)
                                <button type="button" class="ml-1 text-cyan-600 hover:text-cyan-900 underline" onclick="applySuggestedCategory(${data.category_id})">Apply</button>
                            </span>
                        `;
                    }
                })
                .catch(err => console.error(err));
        }, 400);
    }

    if (titleInput) titleInput.addEventListener('input', checkCategorySuggestion);
    if (descInput) descInput.addEventListener('input', checkCategorySuggestion);
    if (imageInput) imageInput.addEventListener('change', checkCategorySuggestion);
}

function applySuggestedCategory(catId) {
    const categorySelect = document.getElementById('id_category');
    if (categorySelect) {
        categorySelect.value = catId;
        const badge = document.getElementById('ai-suggest-badge');
        if (badge) {
            badge.innerHTML = `
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold">
                    <i class="fas fa-check-circle"></i> Applied AI Category
                </span>
            `;
        }
    }
}

document.addEventListener('DOMContentLoaded', setupAiCategoryAssistant);
