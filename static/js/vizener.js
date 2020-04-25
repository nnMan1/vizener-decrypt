let decrypted = document.querySelector("#decrypted_text")
let key = document.querySelector("#key_input")
let encrypted = document.querySelector("#encrypted_text")

function encrypt() {

$.ajax('/encrypt/vizener', {
    method: 'GET',
    data: {
        key: key.value,
        text: decrypted.value
    }
})
.then(
    function success(resopnse) {
        encrypted.value = resopnse
    },

    function fail(data, status) {
        alert('Doslo je do greske');
    }
);
}

function decrypt() {

$.ajax('/decrypt/vizener', {
    method: 'GET',
    data: {
        encrypted: encrypted.value
    }
})
.then(
    function success(response) {
        decrypted.value = response.decrypted
        key.value = response.key
    },

    function fail(data, status) {
        alert('Doslo je do greske');
    }
);
}

document.querySelector("button").addEventListener("click", e => {
    if($('input[name=type]:checked').val() == "decrypt") {
        decrypt()
    } else {
        encrypt()
    }
});

document.getElementById('directions-span').addEventListener('click', function() {
   document.querySelector('#use-directions').classList.toggle('hidden');
});