document.addEventListener('DOMContentLoaded', function () {


  document.querySelectorAll('.like-number').forEach(
    function (div) {
      div.querySelector('button').addEventListener('click', () => {

        id = div.querySelector('.like-number button').dataset.id

        fetch(`/like/${id}`, {
          method: 'PUT',
          body: JSON.stringify({

          })
        }).then(response => response.json()).then(json => {

          if (json["like"]) {
            div.querySelector('.like-number button .heart-like').style.color = "red"
          } else {
            div.querySelector('.like-number button .heart-like').style.color = "gray"
          }
          div.querySelector('.like-number button .number-like').innerHTML = `${json["number_like"]}`

          //div.querySelector('.edit-content').style.display = 'none'
        })
      })

    }
  )


  


});


function load_init() {
  document.querySelectorAll('.show-content').forEach(
    function (div) {
      div.style.display = 'block';
    }
  )
  document.querySelectorAll('.edit-content').forEach(
    function (div) {
      div.style.display = 'none';
    }
  )

}
