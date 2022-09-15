var myForm = document.getElementById('myForm');
myForm.onsubmit = function (e) {

    e.preventDefault();

    var form = new FormData(myForm);

    fetch("http://localhost:5000/register", {
            method: 'POST',
            body: form
        })
        .then(response => response.json())
        .then(data => {
            if(data.status == 'ok'){
                toastr.success(data.message);
                setTimeout(function(){ 
                    window.location.href = 'http://localhost:5000/';
                }, 3000);
            } else {
                toastr.error(data.message);
            }
        });
}