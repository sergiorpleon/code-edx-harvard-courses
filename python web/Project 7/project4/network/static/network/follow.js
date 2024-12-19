document.addEventListener('DOMContentLoaded', function () {


    document.querySelectorAll('.user-info').forEach(
      function (div) {
        if( div.querySelector('#follow-button')){
        div.querySelector('#follow-button').addEventListener('click', () => {
          
          id = div.querySelector('#follow-button').dataset.id
  
          fetch(`/follow/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
  
            })
          }).then(response => response.json()).then(json => {
            if (json["follow"]) {
              div.querySelector('#follow-button').innerHTML = `<span class="btn btn-sm btn-primary">Follow</span>`
            } else {
              div.querySelector('#follow-button').innerHTML = `<span class="btn btn-sm btn-light">Follow</span>`
  
            }
            div.querySelector('.number_of_followers').innerHTML = `<span class="number_of_followers h4">${json["number_follower"]}<small class="ml-1">Followers</small>`
            //div.querySelector('.edit-content').style.display = 'none'
          })
        })
      }})
  });