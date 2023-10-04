


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
