// stub for now so that link from createPuzzle.html isn't broken
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("form");
    form.addEventListener("submit", submitForm);
});

function submitForm(event) {
    event.preventDefault();
    console.log("Form submitted");
    const puzzleName = document.getElementById("name").value;
    const rows = document.getElementById("rows").value;
    const columns = document.getElementById("columns").value;
    //console.log(`Puzzle name: ${puzzleName}, Num Rows: ${rows}, Num Columns: ${columns}`);
    window.location.href = `/puzzle/new/${rows}/${columns}`;
}