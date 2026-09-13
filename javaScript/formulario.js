document.addEventListener("DOMContentLoaded",()=>{
    //validacion de dni 
    const dni = document.getElementById("dni_artesano");
    const error_dni= document.getElementById("error_dni");
    dni.addEventListener("change",()=>{
        if(dni.value.length != 8 || isNaN(dni.value)){
            error_dni.textContent = "El dni debe contener 8 digitos";
        }
        else{
            error_dni.textContent="";
        }
    })
    //validacion de edad
    const edad = document.getElementById("edad_artesano");
    const error= document.getElementById("error_edad");
    edad.addEventListener("change",()=>{
        if(edad.value < 18 ){
            error.textContent= "Debes ser mayor de edad para poder inscribirte";
        }
        else if(edad.value > 100){
            error.textContent="Ingrese una edad valida";
        }
        else{
            error.textContent="";
        }
    })
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
        if (error_dni.textContent !== "" || error.textContent !== "") {
            evento.preventDefault();
            alert("Corrige los errores en rojo antes de enviar tu solicitud");
        }
        if (error_dni.textContent === "" && error.textContent === "") {
            evento.preventDefault(); 
            Swal.fire({
                title: "¡Excelente!",
                text: "El formulario se completó correctamente.",
                icon: "success",
                confirmButtonColor: "#3085d6"
            }).then(() => {
                formulario.submit();
            });
        }
    });
});