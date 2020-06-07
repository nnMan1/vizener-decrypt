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

document.querySelector("#startProgram").addEventListener("click", e => {
    if($('input[name=type]:checked').val() == "decrypt") {
        decrypt()
    } else {
        encrypt()
    }
});

var encryptedTextarea = document.getElementById('encrypted_text');
var decryptedTextarea = document.getElementById('decrypted_text');
var myFile = document.getElementById('myFile');
var useDirections = document.querySelector('#use-directions');
var useInfo = document.querySelector('#use-info');

document.getElementById('directions-span').addEventListener('click', function() {
    useDirections.classList.toggle('hidden');
    if (!useInfo.classList.contains('hidden'))
        useInfo.classList.add('hidden');
});

document.getElementById('info-span').addEventListener('click', function() {
    useInfo.classList.toggle('hidden');
    if (!useDirections.classList.contains('hidden'))
        useDirections.classList.add('hidden');
});

document.getElementById('delete-button').addEventListener('click', function() {
    encryptedTextarea.value= "";
    decryptedTextarea.value = "";
    key.value = "";

});

var reader = new FileReader();
reader.onload = function (e) {
    if (document.getElementById('decrypt').checked)
        encryptedTextarea.value = e.target.result.trim();
    else
        decryptedTextarea.value = e.target.result.trim();
};

myFile.addEventListener('change', function() {
    var file = myFile.files[0];
    reader.readAsText(file);
});

function saveTextAsFile(id)
{
    var textToSave = document.getElementById(id).value;
    if (textToSave) {
        var textToSaveAsBlob = new Blob([textToSave], {type:"text/plain"});
        var textToSaveAsURL = window.URL.createObjectURL(textToSaveAsBlob);
        var fileNameToSaveAs = 'vizener' + '_' + id;

        var downloadLink = document.createElement("a");
        downloadLink.download = fileNameToSaveAs;
        downloadLink.innerHTML = "Download File";
        downloadLink.href = textToSaveAsURL;
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);

        downloadLink.click();
    }
}

function destroyClickedElement(event)
{
    document.body.removeChild(event.target);
}