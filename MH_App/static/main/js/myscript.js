$('#slider1, #slider2, #slider3, #slider4, #slider5').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type: 'GET',
        url: '/plus_cart',
        data: {
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        },
    })
})


$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type: 'GET',
        url: '/minus_cart',
        data: {
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        },
    })
})


$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this
    console.log(id)
    $.ajax({
        type: 'GET',
        url: '/remove_cart',
        data: {
            prod_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        },
    })
})