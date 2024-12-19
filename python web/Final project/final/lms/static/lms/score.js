document.addEventListener('DOMContentLoaded', function () {
    
    document.querySelectorAll('.row-answer').forEach(
        function (div) {
            //Save
            div.querySelector('.btn-save-score').addEventListener('click', () => {
                div.querySelector('.btn-save-score').disabled = true
                const score = div.querySelector('.input-score').value
                const explanation = div.querySelector('.input-explanation').value
                const id = div.querySelector('.btn-save-score').dataset.idanswer

                fetch(`/update_score/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        score: score,
                        explanation: explanation
                    })
                }).then(response => response.json()).then(json => {
                    div.querySelector('.btn-save-score').disabled = false
                })
            })
        });

});


