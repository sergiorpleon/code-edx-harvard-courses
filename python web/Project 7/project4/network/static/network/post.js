document.addEventListener('DOMContentLoaded', function () {


  document.querySelectorAll('.form-content').forEach(

    function (div) {

      div.querySelector('.show-content button').addEventListener('click', () => {
        div.querySelector('.show-content').style.display = 'none'
        div.querySelector('.edit-content').style.display = 'block'
      })

      div.querySelector('.edit-content button').addEventListener('click', () => {
        content = div.querySelector('.edit-content textarea').value
        id = div.querySelector('.edit-content textarea').dataset.id

        fetch(`/posts/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            content: content
          })
        }).then(response => {
          content = div.querySelector('.show-content div').innerHTML = content
          div.querySelector('.show-content').style.display = 'block'
          div.querySelector('.edit-content').style.display = 'none'
        })
      })

    }
  )
  load_init();
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
