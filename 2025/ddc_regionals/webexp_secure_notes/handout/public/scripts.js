document.addEventListener("DOMContentLoaded", () => {
    const propertiesDiv = document.getElementById("properties");
    const addButton = document.getElementById("add-property");

    // Function to create a property field
    const createPropertyField = () => {
        const propertyDiv = document.createElement("div");
        propertyDiv.classList.add("property");

        const propertyInput = document.createElement("input");
        propertyInput.setAttribute("type", "text");
        propertyInput.setAttribute("name", "property[]");
        propertyInput.setAttribute("placeholder", "Property");
        propertyInput.required = true;

        const valueInput = document.createElement("input");
        valueInput.setAttribute("type", "text");
        valueInput.setAttribute("name", "value[]");
        valueInput.setAttribute("placeholder", "Value");
        valueInput.required = true;

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.classList.add("remove-property");
        removeButton.textContent = "-";

        // Append inputs and remove button to the property div
        propertyDiv.appendChild(propertyInput);
        propertyDiv.appendChild(valueInput);
        propertyDiv.appendChild(removeButton);

        // Append the property div to the properties container
        propertiesDiv.appendChild(propertyDiv);
    };

    // Event listener for adding a new property field
    addButton.addEventListener("click", () => {
        createPropertyField();
    });

    // Event listener for removing a property field
    propertiesDiv.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-property")) {
            const propertyDiv = event.target.parentElement;
            propertiesDiv.removeChild(propertyDiv);
        }
    });

    // Create the first property field on load
    createPropertyField();
});
