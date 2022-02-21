$(document).ready(function() {
    $(".dropdown-trigger").dropdown();
    $('.parallax').parallax();
    $('.materialbox').materialbox();


    $('.sidenav').sidenav();
    $('select').formSelect();

    function update_basket_count() {
        longclawclient.basketListCount.get({
            prefix: "/api/",
        }).then(
            value => {
                const count = value.quantity
                if (count > 0) {
                    $('span#basket-item-count').text(count)
                } else {
                    $('span#basket-item-count').text("")
                }
                console.log(value);
            }
        )
    }

    const btn = document.getElementById('add-to-basket-btn');
    const select = document.getElementById('variant-select');

    if (btn !== null) {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const variant_id = select.options[select.selectedIndex].value;
            longclawclient.basketList.post({
                prefix: "/api/",
                data: {
                    variant_id
                }
            }).then(value => {
                update_basket_count()
            })

        });
    }

    $('.slider').slider();
    $('.materialboxed').materialbox();

    $("input.basket_quantity_item").bind('input', function() {
        console.log($(this));
    });

    update_basket_count();

    $("button.basket-delete-details").on('click', function(e) {
        const target = $(this);
        const ids = target.attr('id');
        console.log(ids);
        longclawclient.basketDetail.del({
            prefix: "/api/",
            urlParams: {
                id: parseInt(ids),
            }
        }).then(value => {
            location.reload();
        })
    })
});