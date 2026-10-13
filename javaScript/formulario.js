document.addEventListener("DOMContentLoaded",()=>{
    //validacion de dni 
    const nomyape = document.getElementById("nomyape_artesano");
    const errorNombre = document.getElementById("error_nombre");
    const dni = document.getElementById("dni_artesano");
    const error_dni= document.getElementById("error_dni");
    const tel = document.getElementById("tel_artesano");
    const errorTel = document.getElementById("error_tel");
    const email = document.getElementById("gmail_artesano");
    const errorEmail = document.getElementById("error_email");
    //validacion nombre y apellido
    if (nomyape) {
        nomyape.addEventListener("input", () => {
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

    const fechaNacimiento = document.getElementById("fecha_nacimiento");
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
    const provincia = document.getElementById("provincia_artesano");
    const localidad = document.getElementById("localidad_artesano");
    provincia.addEventListener("change", () => {
        
        let provinciaElegida = provincia.value;
        if (provinciaElegida === "catamarca") {
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="capital">Capital</option>
                <option value="valleViejo">Valle Viejo</option>
                <option value="fme">Fray Mamerto Esquiú</option>
                <option value="belen">Belén</option>
            `;

        } else if (provinciaElegida === "salta") {
            
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="capital">Capital</option>
                <option value="cafayate">Cafayate</option>
                <option value="tartagal">Tartagal</option>
            `;

        } else if (provinciaElegida === "tucuman") {
            
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="capital">Capital</option>
                <option value="tafi">Tafí del Valle</option>
                <option value="yerba">Yerba Buena</option>`;
        } else {
            localidad.innerHTML = `
                <option value="">Seleccione una localidad</option>
                <option value="otro">Otra localidad</option>
            `;
        }
    });
    //Prevenir que el formulario no se envie si los datos no fueron corregidos 
    const formulario = document.querySelector("form");
    formulario.addEventListener("submit", (evento) => {
        const edad = calcularEdad(fechaNacimiento.value);
        if (edad === null || edad < 18 || edad > 100) {
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
        if (typeof Swal !== "undefined") {
            evento.preventDefault(); 
            Swal.fire({
                title: "¡Excelente!",
                text: "El formulario se completó correctamente.",
                icon: "success",
                confirmButtonColor: "#3085d6"
            }).then(() => {
                formulario.submit();
            });
            } else {
            formulario.submit();
            }
    });
});