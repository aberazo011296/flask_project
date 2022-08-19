var myForm = document.getElementById('myForm');
myForm.onsubmit = function (e) {
    // "e" es el evento JS que ocurre cuando enviamos el formulario
    // e.preventDefault() es un método que detiene la naturaleza predeterminada de JavaScript
    e.preventDefault();
    // crea el objeto FormData desde JavaScript y envíalo a través de una solicitud post fetch
    var form = new FormData(myForm);
    // así es como configuramos una solicitud post y enviamos los datos del formulario
    fetch("http://localhost:5000/register", {
            method: 'POST',
            body: form
        })
        .then(response => response.json())
        .then(data => {
            if(data.status == 'ok'){
                toastr.success(data.message);
            } else {
                toastr.error(data.message);
            }
            // toastr.success('Click Button');
            // // for success - green box
            // toastr.success('Success messages');

            // // for errors - red box
            // toastr.error('errors messages');

            // // for warning - orange box
            // toastr.warning('warning messages');

            // // for info - blue box
            // toastr.info('info messages');
        });
}

// var login = document.getElementById('formLogin');

// login.onsubmit = function (e) {

//     e.preventDefault();

//     var form = new FormData(login);

//     fetch("http://localhost:5000/login", {
//             method: 'POST',
//             body: form
//         })
//         .then(response => response.json())
//         .then(data => {
//             if(data.status == 'ok'){
//                 window.location.href = 'http://localhost:5000/dashboard';
//                 toastr.success(data.message);
//             } else {
//                 toastr.error(data.message);
//             }
//         });
// }