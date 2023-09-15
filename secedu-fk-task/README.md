


# PREPARACAO de AMBIENTE::

nvidia-smi


[https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=runfile_local](CudaToolkit 11.8.0)

conda install -c conda-forge cudatoolkit=11.8.0

wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sh cuda_11.8.0_520.61.05_linux.run

#_____________________________________________________________________________#
[https://pypi.org/project/nvidia-cudnn-cu11/#files](Nvidia Cudnn Cu11 8.6.0.163)

wget https://files.pythonhosted.org/packages/64/52/62a198ed717bea2946755b7210e3498db6323b5270fef72099fa414ab2b3/nvidia_cudnn_cu11-8.9.4.25-py3-none-manylinux1_x86_64.whl

pip install nvidia-cudnn-cu11==8.6.0.163


mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_PATH/lib:$CONDA_PREFIX/lib/' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

pip install --upgrade pip

pip install tensorflow==2.13.*

pip install tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

py -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"


### Suporte a GPU Python 3.8	
https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

## Models

{
	'verified': True,
	'distance': 0.30838476846331286,
	'threshold': 0.4,
	'model': 'VGG-Face',
	'detector_backend': 'opencv',
	'similarity_metric': 'cosine',
	'facial_areas': {
		'img1': {
			'x': 13,
			'y': 22,
			'w': 197,
			'h': 197
		},
		'img2': {
			'x': 11,
			'y': 17,
			'w': 172,
			'h': 172
		}
	},
	'time': 7.36
} {
	'verified': False,
	'distance': 0.6607422124361564,
	'threshold': 0.4,
	'model': 'Facenet',
	'detector_backend': 'opencv',
	'similarity_metric': 'cosine',
	'facial_areas': {
		'img1': {
			'x': 13,
			'y': 22,
			'w': 197,
			'h': 197
		},
		'img2': {
			'x': 11,
			'y': 17,
			'w': 172,
			'h': 172
		}
	},
	'time': 7.37
} {
	'verified': False,
	'distance': 0.707853337464952,
	'threshold': 0.3,
	'model': 'Facenet512',
	'detector_backend': 'opencv',
	'similarity_metric': 'cosine',
	'facial_areas': {
		'img1': {
			'x': 13,
			'y': 22,
			'w': 197,
			'h': 197
		},
		'img2': {
			'x': 11,
			'y': 17,
			'w': 172,
			'h': 172
		}
	},
	'time': 6.6
} {
	'verified': False,
	'distance': 0.24123326171161363,
	'threshold': 0.1,
	'model': 'OpenFace',
	'detector_backend': 'opencv',
	'similarity_metric': 'cosine',
	'facial_areas': {
		'img1': {
			'x': 13,
			'y': 22,
			'w': 197,
			'h': 197
		},
		'img2': {
			'x': 11,
			'y': 17,
			'w': 172,
			'h': 172
		}
	},
	'time': 3.95
} {
	'verified': False,
	'distance': 0.3681214373600947,
	'threshold': 0.23,
	'model': 'DeepFace',
	'detector_backend': 'opencv',
	'similarity_metric': 'cosine',
	'facial_areas': {
		'img1': {
			'x': 13,
			'y': 22,
			'w': 197,
			'h': 197
		},
		'img2': {
			'x': 11,
			'y': 17,
			'w': 172,
			'h': 172
		}
	},
	'time': 89.06
}