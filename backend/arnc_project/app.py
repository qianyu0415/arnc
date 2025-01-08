import warnings


# 忽略特定的警告
warnings.filterwarnings('ignore', message='Overwriting tiny_vit_.* in registry with segment_anything.modeling.tiny_vit_sam.tiny_vit_.*')
warnings.filterwarnings('ignore', message='Detectron v2 is not installed')

from arnc import app, db
from arnc.models import Account



# 运行启动后段
if __name__ == '__main__':
    
    app.run(debug=True, port = 6006)