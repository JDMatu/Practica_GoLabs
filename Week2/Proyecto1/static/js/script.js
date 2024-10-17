document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('search').value;
    const resultBox = document.getElementById('resultBox');

    // Simulación de búsqueda
    if (searchTerm) {
        resultBox.innerHTML = `Buscando recetas de "${searchTerm}"...`;
    } else {
        resultBox.innerHTML = "Por favor, ingresa una receta.";
    }
});
