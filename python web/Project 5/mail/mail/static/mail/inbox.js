document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox', 0));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent', 0));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive', 0));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email
  document.querySelector('#compose-form > input').addEventListener('click', send_mail);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Create div for show error message
  if (document.querySelector('#message_error')) {
  } else {
    const message_error = document.createElement('div');
    message_error.id = "message_error";
    document.querySelector('#compose-view>h3').before(message_error);
  }
  document.querySelector('#message_error').innerHTML = "";
}

function load_mailbox(mailbox, id) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  if (mailbox == "mail") {
    // Show one mail
    document.querySelector('#emails-view').innerHTML = `<section id='email-content'></section>`;
    load_mail(mailbox, id);
  } else {
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><section id='emails-list'></section>`;
    load_list_mail(mailbox);

  }
}

function load_mail(mailbox, id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      
      // Put read true
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })

      // Create info mail html
      const div_sender = `<div><strong>From: </strong>${email['sender']}</div>`;
      const div_recipients = `<div><strong>To: </strong>${convert(email['recipients'])}</div>`;
      const div_subject = `<div><strong>Subject: </strong>${email['subject']}</div>`;
      const div_timestamp = `<div><strong>Timestamp: </strong>${email['timestamp']}</div>`;
      document.querySelector('#email-content').innerHTML = div_sender + div_recipients + div_subject + div_timestamp;

      // Reply button
      const rowbutton = document.createElement('div');
      rowbutton.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="inbox">Reply</button>`
      rowbutton.addEventListener('click', function () {

        reply_email(email);
      });
      document.querySelector('#email-content').append(rowbutton)

      // Body mail
      const rowbody = document.createElement('div');
      rowbody.innerHTML = `<div class='border-top mt-3 pt-3'>${email['body']}</div>`;
      document.querySelector('#email-content').append(rowbody);
    });
}

function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Fill composition fields
  document.querySelector('#compose-form>div:nth-child(1)>input').value = `${convert(email['recipients'])}`;
  document.querySelector('#compose-recipients').value = `${email['sender']}`;
  document.querySelector('#compose-subject').value = (email['subject'].startsWith("Re:")) ? email['subject'] : `Re: ${email['subject']}`;
  document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote: ${email['body']}`;

}

function load_list_mail(mailbox) {
  document.querySelector('#emails-list').innerHTML = `<div></div>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      if(emails.length == 0){
        const emptydiv = document.createElement('div');
        emptydiv.innerHTML = `<div class='card'><div class='card-box p-2'>Empty</div></div>`
        document.querySelector('#emails-list').append(emptydiv)
      }
      emails.forEach(email => {

        // Define background row
        let row_style = "style='background-color:#fff'";
        if (email['read']) {
          row_style = "style='background-color:#eee'"
        }

        let rowbutton = "";
        // Prepare html for archive button in inbox view
        if (mailbox == "inbox") {
          rowbutton = `<button class="button-archived btn btn-sm btn-outline-primary ml-1 pt-0 pr-1 pb-0 pl-1">archived</button>`;
        }
        // Prepare html for unarchive button in archive view
        if (mailbox == "archive") {
          rowbutton = `<button class="button-archived btn btn-sm btn-outline-secondary ml-1 pt-0 pr-1 pb-0 pl-1">unarchive</button>`;
        }

        // Creae row for emails list
        const row = document.createElement('div');
        row.innerHTML = `<div class='row border p-2' ` + row_style + `><div class='col-sm-8'><strong>${email['sender']}</strong>&nbsp;${email['subject']}</div><div class='col-sm-4 text-right'><small>${email['timestamp']}</small>` + rowbutton + `</div></div>`
        row.addEventListener('click', function () {
          load_mailbox("mail", email['id']);
        });
        document.querySelector('#emails-list').append(row)

        // Archive and unarchived funcionality
        document.querySelectorAll('.button-archived').forEach(button => {
          button.onclick = function (e) {
            e.stopPropagation()
            fetch(`/emails/${email['id']}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived: mailbox == "inbox" ? true : false
              })
            }).then(response => {
              load_mailbox(mailbox);
            })
          }
        })
      });

    });
}

function send_mail(evt) {
  evt.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  if (recipients == "" || subject == "") {
    // Show message error if empty field
    const message = document.querySelector('#message_error')
    message.innerHTML = `<div class='alert alert-danger mt-1 mt-1'>Empties fields</div>`;
  } else {
    // Call api
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
      .then(response => response.json())
      .then(result => {
        if (result.message) {
          // If susscceful go to sent box
          load_mailbox('sent');
        } else {
          // Show error
          console.log(result.error);
          const message = document.querySelector('#message_error')
          message.innerHTML = `<div class='alert alert-danger mt-1 mt-1'>${result['error']}</div>`;

        }

      });

  }
}

// Convert array recipients to String
function convert(recipients) {
  let result = "";
  console.log(recipients)
  Array.from(recipients).forEach(element => {
    result = result + "," + element;
  });
  return result.slice(1);
}