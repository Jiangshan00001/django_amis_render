function getCookie(cname)
{
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++)
  {
    var c = ca[i].trim();
    if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
  return "";
}

function update_amis_local_to_editor(route_id)
{
    //本地文件到编辑器。需要调用api获取本地文件，写入到编辑器
    $.ajax({
        headers: {"X-CSRFToken":getCookie("csrftoken")},
        type: "get",
       url: "/admin/django_amis_render/amisrenderlist/amis_to_editor/"+route_id+'/',
       async:false,
        dataType: "json",
        //data:{'route_id':route_id},
         success: function(json_obj){
         var storage=window.localStorage;
         storage["store"]=JSON.stringify(json_obj['data']);
        }
    });
    window.location.href="/static/amis-editor-demo/index.html";
}
function update_amis_editor_to_local()
{
    //编辑器内容到本地
    $.ajax({
        headers: {"X-CSRFToken":getCookie("csrftoken")},
        type: "post",
       url: "/admin/django_amis_render/amisrenderlist/update_amis_editor_to_local/",
       async:false,
        dataType: "json",
        data:{'store':window.localStorage['store']},
         success: function(json_obj){
        }
    });
    window.location.href="/admin/django_amis_render/amisrenderlist/";
}

