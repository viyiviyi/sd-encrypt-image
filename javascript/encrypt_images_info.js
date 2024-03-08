lsLoad = false;
onUiUpdate(function () {
  // 获取所有的img标签
  if (lsLoad) return;
  if (!opts) return;
  if (!opts["encrypt_image_is_enable"]) return;
  lsLoad = true;
  let enable = opts["encrypt_image_is_enable"] == "是";
  function renderInfo(txtOrImg2img, isEnable) {
    let info = document.getElementById(
      "encrypt_image_" + txtOrImg2img + "2img_info"
    );
    if (!info) {
      var top = document.getElementById(txtOrImg2img + "2img_neg_prompt");
      if (!top) return;
      var parent = top.parentNode;
      info = document.createElement("div");
      info.style.minWidth = "100%";
      info.style.textAlign = "center";
      info.style.opacity = 0.5;
      info.style.fontSize = ".89em";
      info.id = "encrypt_image_" + txtOrImg2img + "2img_info";
      parent.appendChild(info);
    }
    if (!info) return;
    info.innerHTML = `
<span>${
      isEnable
        ? "图片加密插件已经启用，图片将加密保存在服务器"
        : "图片加密插件已安装但未启用"
    }。
<a rel="noopener noreferrer" target="_blank" href="https://github.com/viyiviyi/sd-encrypt-image">点击查看插件主页</a>
</span>
`;
  }
  renderInfo("txt", enable);
  renderInfo("img", enable);
});
