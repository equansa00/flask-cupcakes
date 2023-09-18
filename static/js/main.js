// Query all cupcakes and append to the list

$(document).ready(function () {
function getCupcakes() {
    axios.get("/api/cupcakes").then(res => {
        for (let cupcake of res.data.cupcakes) {
            // Append each cupcake to a list (assuming you have a list element with id="cupcake-list")
            $("#cupcake-list").append(`<li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}</li>`);
        }
    });
}

// Handle form submission
$("#cupcake-form").submit(function (e) {
    e.preventDefault();
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();

    axios.post("/api/cupcakes", {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    }).then(res => {
        // Append the newly created cupcake to the list
        let cupcake = res.data.cupcake;
        $("#cupcake-list").append(`<li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}</li>`);
    });
});

// Initially fetch all cupcakes
getCupcakes();

});