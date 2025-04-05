function sanitizeHTML(input) {
    // Create a template element to parse the input
    const template = document.createElement('template');
    template.innerHTML = input;
    
    // Define allowed tags and attributes
    const allowedTags = new Set(['b', 'i', 'u', 'strong', 'em', 'p', 'br', 'a', 'ul', 'ol', 'li', 'form', 'input', 'span', 'div', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'img']);
    const allowedAttributes = new Set(['href', 'id']);

    function clean(node) {
        if (node.nodeType === Node.ELEMENT_NODE) {
            // Remove disallowed tags
            if (!allowedTags.has(node.tagName.toLowerCase())) {
                node.remove();
                return;
            }

            // Remove disallowed attributes
            for (let i = node.attributes.length - 1; i >= 0; i--) {
                let attr = node.attributes[i]
                if (!allowedAttributes.has(attr.name.toLowerCase()) || (attr.name.toLowerCase()=='href' && !attr.value.toLowerCase().startsWith("http"))) {
                    node.removeAttribute(attr.name);
                }
            }
        }

        // Recursively clean child nodes
        for (let i = 0; i<node.childNodes.length; i++){
            let child = node.childNodes[i]
            clean(child);
        }
    }
    clean(template.content);
    return template.innerHTML;
}
