helloBtn = document.getElementById("helloBtn");

helloBtn.addEventListener('click', () => {
    console.log("Hello");
    fetch('http:/localhost:3000/call_script').then(
      (response) => response.json()).then((data) => console.log(data));
});
