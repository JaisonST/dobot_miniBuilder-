blockId = 1;
colorArray = [5, 5, 5];

undoBtn = document.getElementById("undoBtn");

// Drag and drop functions 
function dragstart(event) {
    event.target.id = blockId;
    event.dataTransfer.setData("Text", event.target.id);
}

function allowDrop(event) {
    event.preventDefault();
}

function droppoint(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("Text");

    nodeCopy = document.getElementById(data).cloneNode('true');
    nodeCopy.id = blockId;
    blockId++;

    nodeCopy.setAttribute('draggable', false);
    event.target.appendChild(nodeCopy);

    // Update count
    colorArray[colorInput(nodeCopy.classList[1])] -= 1;
    updateId = "count" + colorInput(nodeCopy.classList[1]);
    document.getElementById(updateId).innerHTML = colorArray[colorInput(nodeCopy.classList[1])];

    // Stop draggable from choose array
    if (colorArray.includes(0)) {
        stopId = "count" + colorArray.indexOf(0);
        chooseArrayBlock = document.getElementById(stopId).parentElement.childNodes[1];
        console.log(chooseArrayBlock);
        chooseArrayBlock.setAttribute('draggable', false);
    }

    // Undo enable 
    undoBtn.removeAttribute("disabled");
}

cols = document.getElementsByClassName('column');
Array.from(cols).forEach(element => {
    element.addEventListener('drop', (event) => {
        droppoint(event)
    })

    element.addEventListener('dragover', (event) => {
        allowDrop(event);
    })

    // Clear matrix 
    clearAll = document.getElementById('clearAll');
    clearAll.addEventListener('click', () => {
        location.reload();
    })
});

// Encoding and validating input
function validateInput() {
    buildNodes = document.getElementById("buildArea").getElementsByClassName('row');
    input = [];
    rowN = 0;
    Array.from(buildNodes).reverse().forEach(element => {
        cols = element.getElementsByClassName("column");
        row = [];
        colN = 0;
        Array.from(cols).forEach(col => {
            if (!col.hasChildNodes()) {
                row.push(4);
            }
            else {
                if (rowN > 0 && input[rowN - 1][colN] == 4) {
                    error.innerHTML = "Invalid input";
                    return ;
                }
                row.push(colorInput(col.childNodes[0].classList[1]));
            }
            colN += 1;
        });
        input.push(row);
        rowN += 1;
    });

    console.log(input.reverse());
    console.log("Je", JSON.stringify(input.reverse()));

    fetch('/call_script', { method: 'POST', headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }, body: JSON.stringify({"input": input.reverse()})}).then(
        (response) => response.json()).then((data) => console.log(data));
}


// Encoding function
function colorInput(colorClass) {
    switch (colorClass) {
        case 'red': return 0;

        case 'green': return 1;

        case 'blue': return 2;
    }
}

// Add: Multiple undos
function undo() {
    nodeCopy = document.getElementById(blockId - 1);
    nodeCopy.remove();

    colorArray[colorInput(nodeCopy.classList[1])] += 1;
    updateId = "count" + colorInput(nodeCopy.classList[1]);
    document.getElementById(updateId).innerHTML = colorArray[colorInput(nodeCopy.classList[1])];

    undoBtn.setAttribute("disabled", true);
}
