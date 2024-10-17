<script>
    document.getElementById('filter-button').addEventListener('click', function() {
        const selectedCategory = document.getElementById('category-filter').value;
        const cards = document.querySelectorAll('.receta-card');

        cards.forEach(card => {
            // Aquí deberías tener una forma de obtener la categoría de la receta
            const category = card.getAttribute('data-category'); // Asegúrate de agregar el atributo data-category en las tarjetas
            if (selectedCategory === 'all' || category === selectedCategory) {
                card.style.display = 'block'; // Mostrar la tarjeta
            } else {
                card.style.display = 'none'; // Ocultar la tarjeta
            }
        });
    });
</script>
