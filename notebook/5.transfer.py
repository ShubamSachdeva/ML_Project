#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import torch
import time
import pickle
import matplotlib.pyplot as plt
from collections import OrderedDict
from torch.autograd import Variable
from pathlib import Path
from tqdm import tqdm

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


pix2pixhd_dir = Path('../src/pix2pixHD/')

import sys
sys.path.append(str(pix2pixhd_dir))

#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


from data.data_loader import CreateDataLoader
from models.models import create_model
import util.util as util
from util.visualizer import Visualizer
from util import html


# In[ ]:


with open('../data/test_opt.pkl', mode='rb') as f:
    opt = pickle.load(f)


opt.use_encoded_image='true'
iter_path = os.path.join(opt.checkpoints_dir, opt.name, 'iter.txt')


# In[ ]:


data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
visualizer = Visualizer(opt)
# create website
web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))


# In[ ]:


model = create_model(opt)


# In[ ]:


for data in tqdm(dataset):
    minibatch = 1
    generated = model.inference(data['label'], data['inst'])

    visuals = OrderedDict([('input_label', util.tensor2label(data['label'][0], opt.label_nc)),
                           ('synthesized_image', util.tensor2im(generated.data[0]))])
    img_path = data['path']
    visualizer.save_images(webpage, visuals, img_path)
webpage.save()
torch.cuda.empty_cache()


# In[ ]:




