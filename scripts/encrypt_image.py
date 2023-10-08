from preload import EncryptedImage,get_sha256

from modules import shared

password = getattr(shared.cmd_opts, 'encrypt_pass', None)

if password:
    EncryptedImage.password = password
    section = ("encrypt_image",'图片加密' if shared.opts.localization == 'zh_CN' else "encrypt image" )
    shared.opts.add_option(
        "encrypt_pass_hash",
        shared.OptionInfo(
            default=get_sha256(password),
            label='图片解密密码的哈希值, 别改!' if shared.opts.localization == 'zh_CN' else "encrypt image hash password",
            section=section,
        ),
    )
    shared.opts.data['encrypt_pass_hash'] = get_sha256(password)