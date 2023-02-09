const form = document.querySelector('#form');


let docentes = [];
let editar = false;
let docenteId = null;


window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/jonathan/docente")
    const data = await response.json()
    docentes = data
    console.log(data)
    renderDocente(docentes)
})


form.addEventListener('submit', async e => {
    e.preventDefault()

    const nombre = form['nombre'].value;
    const apellido = form['apellido'].value;
    const catedra = form['catedra'].value;
    const facultad = form['facultad'].value;
    const paralelo = form['paralelo'].value;
    const jornada = form['jornada'].value;

    console.log(nombre, apellido, catedra, facultad, paralelo, jornada)

    if (!editar) {
        const response = await fetch('/jonathan/docente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellido,
                catedra,
                facultad,
                paralelo,
                jornada
            })
        })

        const data = await response.json();
        console.log(data);
        docentes.unshift(data);
        renderDocente(docentes)
        form.reset()
    }
    else {
        const response = await fetch(`/jonathan/docente/${docenteId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellido,
                catedra,
                facultad,
                paralelo,
                jornada
            })
        })

        const updataDocente = await response.json()
        docentes = docentes.map(docente => docente.id === updataDocente.id ? updataDocente : docente)
        renderDocente(docentes)
        editar = false
        docenteId = null
    }

    renderDocente(docentes);
    form.reset();

});

function renderDocente(docente) {
    const docenteList = document.querySelector('#docenteList')
    docenteList.innerHTML = ""
    docentes.forEach(docente => {
        const docenteItem = document.createElement('li')
        docenteItem.classList = 'list-group list-group-item-dark my-2'
        docenteItem.innerHTML = `
        <header>
        <div>
        <h3>${docente.nombre}  ${docente.apellido}</h3>
        </div>
        </header>
        <body    >
        <p>
        ${docente.catedra}
        </p>
         <p>
        ${docente.facultad}
        </p>
         <p>
        ${docente.paralelo}
        </p>
         <p>
        ${docente.jornada}
        </p>
        <div class="d-flex align-items-center;">
            <button class="btn-delete btn btn-danger">borrar</button>
            <button class="btn-edit btn  btn-danger "  >actualizar</button>
        </div>
        
        </body>
        `

        const btnDelete = docenteItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async () => {
            console.log(docente.id)
            const response = await fetch(`/jonathan/docente/${docente.id}`, {
                method: 'DELETE',
            })
            const data = await response.json()
            console.log(data)
            docentes = docentes.filter(docente => docente.id !== data.id)
            renderDocente(docentes)
        })

        const btnEdit = docenteItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async () => {
            console.log(docente.id)
            const response = await fetch(`/jonathan/docente/${docente.id}`)
            const data = await response.json()

            form['nombre'].value = data.nombre;
            form['apellido'].value = data.apellido;
            form['catedra'].value = data.catedra;
            form['facultad'].value = data.facultad;
            form['paralelo'].value = data.paralelo;
            form['jornada'].value = data.jornada;

            editar = true
            console.log(data)
            docenteId = docente.id
        })





        console.log(docenteItem);
        docenteList.append(docenteItem);
    })
}