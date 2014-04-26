id_generator
============

O id_generator é um script indepotente que criará uma lista de ids de shows
para o magro percorrer. Esta lista será salva no CouchDB e terá o seguinte "schema":

[{
    show_id: 1,
    exists: null, //pode se tornar true ou false depois do magro verificar a existência do mesmo
    last_checked: 0 
}]
