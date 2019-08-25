$(function () {

  /* Functions */

  var loadForm = function () {      /* load CRUD 對應的 modal form */
    var btn = $(this);
    // alert(btn.attr("data-url"));
    $.ajax({
      url: btn.attr("data-url"),    /* 要 get 的   url */
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html(""); /* request 前,設定 */
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form); /* 取出後,bind data 值*/
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        // alert(XMLHttpRequest.status);
        // alert(XMLHttpRequest.readyState);
        // alert(textStatus);
      }
    });
  };

  var saveForm = function () {    /* 執行 modal form 對應之 CRUD */
    var form = $(this);
    // alert('saveform');
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        // alert(XMLHttpRequest.status);
        // alert(XMLHttpRequest.readyState);
        // alert(textStatus);
      }
    });
    return false;
  };

  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

});
