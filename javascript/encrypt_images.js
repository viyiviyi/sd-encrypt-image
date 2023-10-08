const encrypt_images_loading_list = window.encrypt_images_loading_list || [];
onUiUpdate(function () {
  // 获取所有的img标签
  if (!opts) return;
  if (!opts["encrypt_pass_hash"]) return;
  let password = opts["encrypt_pass_hash"];

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  function get_range(input, offset, range_len = 4) {
    if (offset + range_len < input.length) {
      return input.substring(offset, offset + range_len);
    } else {
      return (
        input.substring(offset) +
        input.substring(0, range_len - (input.length - offset))
      );
    }
  }

  async function get_sha256(input) {
    // nodejs
    // const hash = crypto.createHash("sha256");
    // hash.update(input);
    // return hash.digest("hex");
    // 浏览器
    const data = input;
    // 将数据编码为 Uint8Array
    const encoder = new TextEncoder();
    const dataUint8Array = encoder.encode(data);
    // 计算 SHA-256 哈希值
    async function sha256(data) {
      const hashBuffer = await crypto.subtle.digest("SHA-256", data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const hashHex = hashArray
        .map((byte) => byte.toString(16).padStart(2, "0"))
        .join("");
      return hashHex;
    }
    // 调用 sha256 函数计算哈希值
    return await sha256(dataUint8Array).then((hash) => {
      return hash;
    });
  }

  async function shuffle_arr(arr, key) {
    var sha_key = await get_sha256(key);
    var key_offset = 0;
    for (var i = 0; i < arr.length; i++) {
      var to_index =
        parseInt(get_range(sha_key, key_offset, 8), 16) % (arr.length - i);
      key_offset += 1;
      if (key_offset >= sha_key.length) {
        key_offset = 0;
      }
      var temp = arr[i];
      arr[i] = arr[to_index];
      arr[to_index] = temp;
    }
    return arr;
  }
  async function encrypt_image(image, psw) {
    var x_arr = [];
    for (var i = 0; i < image.width; i++) {
      x_arr.push(i);
    }
    await shuffle_arr(x_arr, psw);
    var y_arr = [];
    for (var i = 0; i < image.height; i++) {
      y_arr.push(i);
    }
    await shuffle_arr(y_arr, await get_sha256(psw));
    var pixels = image.data;
    // var offfset = 0;
    // for (var x = 0; x < image.width; x++) {
    //   for (var y = 0; y < image.height; y++) {
    //     var arr = get_range(psw, offfset, 6);
    //     offfset += 1;
    //     if (offfset >= psw.length) offfset = 0;
    //     xy = (y * image.width + x) * 4;
    //     pixels[xy + 0] = pixels[xy + 0] ^ parseInt(arr.substring(0, 2), 16);
    //     pixels[xy + 1] = pixels[xy + 1] ^ parseInt(arr.substring(2, 4), 16);
    //     pixels[xy + 2] = pixels[xy + 2] ^ parseInt(arr.substring(4), 16);
    //   }
    // }
    let temp = 0;
    for (var x = 0; x < image.width; x++) {
      for (var y = 0; y < image.height; y++) {
        var index = (y * image.width + x) * 4;
        var x_index = (y_arr[y] * image.width + x_arr[x]) * 4;
        for (var o = 0; o < 4; o++) {
          temp = pixels[index + o];
          pixels[index + o] = pixels[x_index + o];
          pixels[x_index + o] = temp;
        }
      }
    }
    return pixels;
  }
  async function dencrypt_image(image, psw) {
    var x_arr = [];
    for (var i = 0; i < image.width; i++) {
      x_arr.push(i);
    }
    await shuffle_arr(x_arr, psw);
    var y_arr = [];
    for (var i = 0; i < image.height; i++) {
      y_arr.push(i);
    }
    await shuffle_arr(y_arr, await get_sha256(psw));
    var pixels = image.data;
    let temp = 0;
    for (var x = 0; x < image.width; x++) {
      var _x = image.width - x - 1;
      for (var y = 0; y < image.height; y++) {
        var _y = image.height - y - 1;
        var index = (_y * image.width + _x) * 4;
        var x_index = (y_arr[_y] * image.width + x_arr[_x]) * 4;
        for (var o = 0; o < 4; o++) {
          temp = pixels[index + o];
          pixels[index + o] = pixels[x_index + o];
          pixels[x_index + o] = temp;
        }
      }
    }
    // var offfset = 0;
    // for (var x = 0; x < image.width; x++) {
    //   for (var y = 0; y < image.height; y++) {
    //     var arr = get_range(psw, offfset, 6);
    //     offfset += 1;
    //     if (offfset >= psw.length) offfset = 0;
    //     xy = (y * image.width + x) * 4;
    //     pixels[xy + 0] =
    //       pixels[xy + 0] ^ (parseInt(arr.substring(0, 2), 16) & 0xff);
    //     pixels[xy + 1] =
    //       pixels[xy + 1] ^ (parseInt(arr.substring(2, 4), 16) & 0xff);
    //     pixels[xy + 2] =
    //       pixels[xy + 2] ^ (parseInt(arr.substring(4), 16) & 0xff);
    //   }
    // }
    return pixels;
  }

  async function getImgSizee(src) {
    return new Promise((res) => {
      var temp_img = new Image();
      temp_img.src = src;
      if (temp_img.complete) {
        res({ width: temp_img.width, height: temp_img.height });
      } else {
        temp_img.onload = function () {
          res({ width: temp_img.width, height: temp_img.height });
        };
      }
    });
  }
  async function bandEvent(imgDom) {
    let img = new Image();
    img = imgDom;
    if (!img.src.startsWith("http")) return;
    // 设置 Canvas 的宽高与图片一致
    let size = await getImgSizee(img.src);
    canvas.width = size.width;
    canvas.height = size.height;
    // 将图片绘制到 Canvas 上
    ctx.drawImage(img, 0, 0);
    // 获取图片的像素数据
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    imageData.data = await dencrypt_image(imageData, password);
    // 将调整后的像素数据重新绘制到 Canvas 上
    ctx.putImageData(imageData, 0, 0);
    // 将还原的图片写回img
    img.src = canvas.toDataURL();
  }
  var imgs = [];
  // txt2img output
  var box = document.getElementById("txt2img_gallery");
  if (box) {
    imgs.push(...box.getElementsByTagName("img"));
  }
  box = document.getElementById("img2img_gallery");
  if (box) {
    imgs.push(...box.getElementsByTagName("img"));
  }
  box = document.getElementById(
    "image_browser_tab_txt2img_image_browser_gallery"
  );
  if (box) {
    imgs.push(...box.getElementsByTagName("img"));
  }
  box = document.getElementById("lightboxModal");
  if (box) {
    imgs.push(...box.getElementsByTagName("img"));
  }
  // img2img output
  for (var i = 0; i < imgs.length; i++) {
    // 给每个img标签添加load事件处理函数
    bandEvent(imgs[i]);
  }
});
