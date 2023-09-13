

pelicula_recomendada(feliz, accion, 'Rápido y Furioso').
pelicula_recomendada(feliz, fantasia, 'Harry Potter y la Piedra Filosofal').
pelicula_recomendada(feliz, amor, 'Cartas a Julieta').
pelicula_recomendada(feliz, comedia, 'Shrek I').

pelicula_recomendada(triste, accion, 'Gladiador').
pelicula_recomendada(triste, fantasia, 'Up: una aventura de altura').
pelicula_recomendada(triste, amor, 'Orgullo y Prejuicio').
pelicula_recomendada(triste, comedia, 'Un espia y medio').

pelicula_recomendada(enojado, accion, 'Busqueda implacable').
pelicula_recomendada(enojado, fantasia, 'Jurassic Park').
pelicula_recomendada(enojado, amor, 'The Notebook').
pelicula_recomendada(enojado, comedia, 'Una esposa de mentira').

obtener_pelicula_recomendada(Animo, Genero, PeliculaRecomendada) :-
    findall(Pelicula, pelicula_recomendada(Animo, Genero, Pelicula), Peliculas),
    nth0(0, Peliculas, PeliculaRecomendada).
