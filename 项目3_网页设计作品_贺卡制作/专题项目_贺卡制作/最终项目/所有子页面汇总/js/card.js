let selectedTextId = null;
let startX = 0, startY = 0; 
let initialElementX = 0, initialElementY = 0; 
let isDragging = false;

function getBackgroundFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('background');
  }
  
  window.onload = function() {
    const container = document.getElementById("container");
    const backgroundImage = getBackgroundFromURL(); 
  
    if (backgroundImage) {
      container.style.backgroundImage = `url(${backgroundImage})`;
    } else {
      const defaultBackground = './images/Newyear/1.png';
      container.style.backgroundImage = `url(${defaultBackground})`;
    }
  
    container.style.backgroundSize = "cover";
    container.style.backgroundPosition = "center";
    container.setAttribute("data-background", backgroundImage || './images/Newyear/1.png'); 
  };
  

function selectText(id) {
    selectedTextId = id === 'title' ? 'titleText' : 'descriptionText';
    document.getElementById("textOptions").style.display = "flex";
    document.getElementById("contentInput").value = document.getElementById(selectedTextId).innerText;
}


function updateContent() {
    if (selectedTextId) {
        const content = document.getElementById("contentInput").value;
        document.getElementById(selectedTextId).innerText = content;
    }
}

function updateFont() {
    if (selectedTextId) {
        const font = document.getElementById("fontSelect").value;
        document.getElementById(selectedTextId).style.fontFamily = font;
    }
}

function updateFontSize() {
    if (selectedTextId) {
        const fontSize = document.getElementById("fontSize").value;
        document.getElementById(selectedTextId).style.fontSize = fontSize + "px";
    }
}

function updateColor() {
    if (selectedTextId) {
        const color = document.getElementById("colorPicker").value;
        document.getElementById(selectedTextId).style.color = color;
    }
}


document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('mousedown', initiateDrag);
    item.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

function initiateDrag(e) {
    e.preventDefault();
    e.stopPropagation();

    if (selectedTextId) {
        const element = document.getElementById(selectedTextId);

      
        startX = e.clientX;
        startY = e.clientY;

   
        const elementRect = element.getBoundingClientRect();
        const containerRect = document.getElementById("container").getBoundingClientRect();
        initialElementX = elementRect.left - containerRect.left;
        initialElementY = elementRect.top - containerRect.top;

        document.onmousemove = startDragging;
        document.onmouseup = closeDragElement;
    }
}

function startDragging(e) {
    e.preventDefault();
    if (!isDragging) {
        isDragging = true;
    }

    if (selectedTextId && isDragging) {
        const element = document.getElementById(selectedTextId);
        const container = document.getElementById("container");

    
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;

   
        const containerRect = container.getBoundingClientRect();
        const elementRect = element.getBoundingClientRect();


        let newLeft = initialElementX + deltaX;
        let newTop = initialElementY + deltaY;

      
        if (newTop < 0) newTop = 0; 
        if (newTop + elementRect.height > containerRect.height) {
            newTop = containerRect.height - elementRect.height;
        }
        if (newLeft < 0) newLeft = 0;
        if (newLeft + elementRect.width > containerRect.width) {
            newLeft = containerRect.width - elementRect.width;
        }


        element.style.position = 'absolute';
        element.style.top = newTop + "px";
        element.style.left = newLeft + "px";
    }
}

function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
    isDragging = false;
}



function saveAsPDF() {
    const container = document.getElementById("container");
    html2canvas(container, {
        backgroundColor: null,
        allowTaint: false,
        useCORS: true,
        scale: 4,
        dpi: window.devicePixelRatio * 4, 
    }).then(canvas => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "mm", "a4");

        
        const pdfWidth = pdf.internal.pageSize.width;
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("Newyear.pdf");
    }).catch(error => {
        console.error("Error while generating PDF: ", error);
    });
}





function changeBackground(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("container").style.backgroundImage = `url(${e.target.result})`;
            document.getElementById("container").style.backgroundSize = "cover";
            document.getElementById("container").style.backgroundPosition = "center";
        };
        reader.readAsDataURL(file);
    }
}




