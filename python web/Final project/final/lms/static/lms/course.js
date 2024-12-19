document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.row-course').forEach(
        function (div) {
            //Delete topic
            div.querySelector('.btn-delete-topic').addEventListener('click', () => {
                const topic_id = div.querySelector('.btn-delete-topic').dataset.idtopic

                fetch(`/delete_topic/${topic_id}`, {
                    method: 'DELETE',
                }).then(response => response.json()).then(json => {
                    div.innerHTML = ""
                    div.style.display = "none"
                })
            });


            //Update topic
            div.querySelector('.btn-update-topic').addEventListener('click', () => {
                console.log("entro");

                const title = div.querySelector('.show-title').innerHTML
                div.querySelector('.show-title').style.display = 'none'
                div.querySelector('.edit-title').style.display = 'block'
                div.querySelector('.edit-title').value = title
                div.querySelector('.btn-save-topic').style.display = 'block'
                div.querySelector('.btn-update-topic').style.display = 'none'
                div.querySelector('.btn-delete-topic').style.display = 'none'

            });

            //Save topic
            div.querySelector('.btn-save-topic').addEventListener('click', () => {
                const title = div.querySelector('.edit-title').value
                const id = div.querySelector('.btn-save-topic').dataset.idtopic

                fetch(`/update_topic/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        title: title
                    })
                }).then(response => response.json()).then(json => {
                    div.querySelector('.show-title').style.display = 'block'
                    div.querySelector('.show-title').innerHTML = json["title"]
                    div.querySelector('.edit-title').style.display = 'none'
                    div.querySelector('.btn-update-topic').style.display = 'block'
                    div.querySelector('.btn-save-topic').style.display = 'none'
                    div.querySelector('.btn-delete-topic').style.display = 'block'
                })
            })
        });


    document.querySelectorAll('.row-course .row-element').forEach(
        function (div) {

            div.querySelector('.btn-delete-element').addEventListener('click', () => {
                console.log("entro111");
                const id = div.querySelector('.btn-delete-element').dataset.id;
                const state = div.querySelector('.btn-delete-element').dataset.type;

                //Delete label
                if (state == "label") {
                    fetch(`/delete_label/${id}`, {
                        method: 'DELETE',
                    }).then(response => response.json()).then(json => {
                        div.innerHTML = ""
                        div.style.display = 'none'
                    });
                }
                //Delete page
                if (state == "page") {
                    fetch(`/delete_page/${id}`, {
                        method: 'DELETE',
                    }).then(response => response.json()).then(json => {
                        div.innerHTML = ""
                        div.style.display = 'none'
                    });
                }
                //Delete task
                if (state == "task") {
                    fetch(`/delete_task/${id}`, {
                        method: 'DELETE',
                    }).then(response => response.json()).then(json => {
                        div.innerHTML = ""
                        div.style.display = 'none'
                    });
                }
            });

        });




    const parent_t = document.querySelector('.parent-topics');
    const children_t = parent_t.querySelectorAll('.row-course');
    children_t.forEach((child_t, index) => {
        child_t.querySelector(".btn-up-topic").addEventListener('click', () => {
            
            //Calling api that moves topic one position up to down depending on the type of movement
            const id = child_t.querySelector('.btn-up-topic').dataset.idtopic
            fetch(`/move_topic/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    direction: "up"
                })
            }).then(response => response.json()).then(json => {
                //Exchange topic with the one above
                const elementoAnterior = child_t.previousElementSibling;
                if (elementoAnterior) {
                    elementoAnterior.before(child_t);
                }
            })

        });



        child_t.querySelector(".btn-down-topic").addEventListener('click', () => {
            
            //Calling api that moves topic one position up to down depending on the type of movement
            const id = child_t.querySelector('.btn-down-topic').dataset.idtopic
            fetch(`/move_topic/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    direction: "down"
                })
            }).then(response => response.json()).then(json => {
                //Exchange topic with the one below
                const elementoAnterior = child_t.nextElementSibling;
                if (elementoAnterior) {
                    elementoAnterior.after(child_t);
                }
            })

        });

        const parent_e = child_t.querySelector('.parent-elements');
        const children_e = parent_e.querySelectorAll('.row-element');
        children_e.forEach((child_e, index) => {

            child_e.querySelector(".btn-up-element").addEventListener('click', (e) => {
                e.preventDefault
                //Calling api that moves element(label, topic, task) one position up to down depending on the type of movement
                const id = child_e.querySelector('.btn-up-element').dataset.id
                const type = child_e.querySelector('.btn-up-element').dataset.type
                fetch(`/move_element/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        type: type,
                        direction: "up"
                    })
                }).then(response => response.json()).then(json => {
                    //Exchange topic with the one above
                    const elementoAnterior = child_e.previousElementSibling;
                    if (elementoAnterior) {
                        elementoAnterior.before(child_e);
                    }
                })
            });

        });
        children_e.forEach((child_e, index) => {
            child_e.querySelector(".btn-down-element").addEventListener('click', (e) => {
                e.preventDefault

                //Calling api that moves element(label, topic, task) one position up to down depending on the type of movement
                const type = child_e.querySelector('.btn-down-element').dataset.type
                const id = child_e.querySelector('.btn-down-element').dataset.id
                fetch(`/move_element/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        type: type,
                        direction: "down"
                    })
                }).then(response => response.json()).then(json => {
                    //Exchange topic with the one below
                    const elementoAnterior = child_e.nextElementSibling;
                    if (elementoAnterior) {
                        elementoAnterior.after(child_e);
                    }
                })
            });
        });
    });







    load_init();
});


function load_init() {
    document.querySelectorAll('.row-course').forEach(
        function (div) {
            div.querySelector('.show-title').style.display = 'block'
            div.querySelector('.btn-update-topic').style.display = 'block'
            div.querySelector('.edit-title').style.display = 'none'
            div.querySelector('.btn-save-topic').style.display = 'none'
        }
    )


};