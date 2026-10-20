document.addEventListener("DOMContentLoaded",()=>{
    //validacion de dni 
    const nomyape = document.getElementById("id_nombre_apellido");
    const errorNombre = document.getElementById("error_nombre");
    const dni = document.getElementById("id_dni");
    const error_dni= document.getElementById("error_dni");
    const tel = document.getElementById("id_telefono");
    const errorTel = document.getElementById("error_tel");
    const email = document.getElementById("id_email");
    const errorEmail = document.getElementById("error_email");
    //validacion nombre y apellido
    if (nomyape) {
        nomyape.addEventListener("input", () => {
            nomyape.value = nomyape.value.replace(/[0-9]/g, '');
            if (nomyape.value.trim().length < 3) {
                errorNombre.textContent = "El nombre y apellido no puede ser tan corto";
            } else {
                errorNombre.textContent = "";
            }
        });
    }
    //validacon dni
    dni.addEventListener("change",()=>{
        if(dni.value.length != 8 || isNaN(dni.value)){
            error_dni.textContent = "El DNI debe contener 8 digitos";
        }
        else{
            error_dni.textContent="";
        }
    })
    //validacion de edad

    const fechaNacimiento = document.getElementById("id_fecha_nacimiento");
    fechaNacimiento.type = "date";
    const errorFecha = document.getElementById("error_fecha");
    function calcularEdad(fechaString) {
        const fechaIngresada = new Date(fechaString);
        const hoy = new Date();

        if (isNaN(fechaIngresada.getTime())) {
            return null;
        }

        let edad = hoy.getFullYear() - fechaIngresada.getFullYear();
        const mes = hoy.getMonth() - fechaIngresada.getMonth();

        if (mes < 0 || (mes === 0 && hoy.getDate() < fechaIngresada.getDate())) {
            edad--;
        }

        return edad;
    }
    fechaNacimiento.addEventListener("change",()=>{
        const edad = calcularEdad(fechaNacimiento.value);
        if(edad === null){
            errorFecha.textContent= "Ingrese una fecha valida";
        }
        else if (edad < 0) {
            errorFecha.textContent = "La fecha no puede ser mayor a la actual";
        }
        else if(edad < 18){
            errorFecha.textContent="Debe ser mayor de 18 para inscribirte";
        }
        else if (edad > 100){
            errorFecha.textContent="Ingrese una fecha de nacimiento valida";
        }
        else{
            errorFecha.textContent=""
        }
    })

    //validacion de numero de telefono
    tel.addEventListener("input",()=>{
        const telRegex = /^[0-9\s\-\+\(\)]{6,20}$/;
        if (!telRegex.test(tel.value.trim())) {
            errorTel.textContent = "Ingrese un numero de telefono valido";
        } else {
            errorTel.textContent = "";
        }
    });
    //validacion de correo electronico
    email.addEventListener("input", () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value.trim())) {
            errorEmail.textContent = "Ingrese un correo electronico valido.";
        } else {
            errorEmail.textContent = "";
        }
    });
    //Provincias con sus correspondientes localidades
    const provincia = document.getElementById("id_provincia");
    const localidad = document.getElementById("id_localidad");
    provincia.addEventListener("change", () => {
        let provinciaElegida = provincia.value;
        if (provinciaElegida === "Catamarca") {
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="Capital">Capital</option>
                <option value="Valle Viejo">Valle Viejo</option>
                <option value="Fray Mamerto Esquiu">Fray Mamerto Esquiú</option>
                <option value="Belen">Belén</option>
            `;

        } else if (provinciaElegida === "Salta") {
            
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="Capital">Capital</option>
                <option value="Cafayate">Cafayate</option>
                <option value="Tartagal">Tartagal</option>
            `;

        } else if (provinciaElegida === "Tucuman") {
            
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="Capital">Capital</option>
                <option value="Tafi del Valle">Tafí del Valle</option>
                <option value="Yerba Buena">Yerba Buena</option>`;
        } else {
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="Otra">Otra localidad</option>
            `;
        }
    });
    //Prevenir que el formulario no se envie si los datos no fueron corregidos 
    const formulario = document.querySelector("form");
    formulario.addEventListener("submit", (evento) => {
        const edad = calcularEdad(fechaNacimiento.value);
        if (edad === null || edad < 18 || edad > 100 || edad < 0){
            errorFecha.textContent = "Debe ingresar una fecha de nacimiento valida";
        }
        const errores = 
            errorNombre.textContent !== "" ||
            error_dni.textContent !== "" ||
            errorFecha.textContent !== "" ||
            errorTel.textContent !== "" ||
            errorEmail.textContent !== "";
        if (errores) {
            evento.preventDefault();
            alert("Corrige los errores antes de enviar tu solicitud");
        }
    });
});