


  $(document).on('change', '#post-form',function(e){
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:'{% url "ajaxcolor" %}',
          data:{
              productid:$('#productid').val(),
              size:$('#size').val(),
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
              action: 'post'
          },
          dataType : 'json',
          success: function (res) {
              $('#appendHere').html(res.data);
          },
          error: function (res) {
              alert("Got an error dude " + res.data);
          }
      });
  });

  ;(function(){
    const modal = new bootstrap.Modal(document.getElementById('modal'))

    htmx.on('htmx:afterSwap',(e) =>{
        if(e.detail.target.id === "dialog")
            modal.show()
    })

    htmx.on('htmx:beforeSwap',(e) =>{
        if(e.detail.target.id === "dialog" && !e.detail.xhr.response)
            modal.show()
    })

    htmx.on('hidden.bs.modal',(e) =>{
       document.getElementById('dialog').innerHTML = ''
    })

  })

  
