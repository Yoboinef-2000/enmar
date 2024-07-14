document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded');
    const textarea = document.getElementById('description');
    const preview = document.getElementById('markdown-preview');
    
    console.log('Textarea:', textarea);
    console.log('Preview:', preview);

    function updatePreview() {
        console.log('Updating preview');
        const markdownText = textarea.value;
        console.log('Markdown text:', markdownText);
        const html = marked.parse(markdownText);
        console.log('Parsed HTML:', html);
        preview.innerHTML = html;
    }

    textarea.addEventListener('input', updatePreview);

    // Initial preview
    updatePreview();
});