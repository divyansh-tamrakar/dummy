var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log('Anonymous User')
        } else {
            console.log('Welcome back,', user)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data....')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })

    .then((response) => {
        return response.json()
    })

    .then((response) => {
        console.log('data:', data)
    })
}