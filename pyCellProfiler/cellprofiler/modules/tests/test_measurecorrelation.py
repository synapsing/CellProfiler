'''test_measurecorrelation - test the MeasureCorrelation module
CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Developed by the Broad Institute
Copyright 2003-2009

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''
__version__="$Revision$"

import base64
import numpy as np
from StringIO import StringIO
import unittest
import zlib

import cellprofiler.pipeline as cpp
import cellprofiler.cpmodule as cpm
import cellprofiler.cpimage as cpi
import cellprofiler.measurements as cpmeas
import cellprofiler.objects as cpo
import cellprofiler.workspace as cpw
import cellprofiler.modules.measurecorrelation as M

IMAGE1_NAME = 'image1'
IMAGE2_NAME = 'image2'
OBJECTS_NAME = 'objects'

class TestMeasureCorrelation(unittest.TestCase):
    def make_workspace(self, image1, image2, objects=None):
        '''Make a workspace for testing ApplyThreshold'''
        module = M.MeasureCorrelation()
        image_set_list = cpi.ImageSetList()
        image_set = image_set_list.get_image_set(0)
        for image_group, name, image in zip(module.image_groups,
                                           (IMAGE1_NAME,IMAGE2_NAME),
                                           (image1, image2)):
            image_group.image_name.value = name
            image_set.add(name, image) 
        object_set = cpo.ObjectSet()
        if objects is None:
            module.images_or_objects.value = M.M_IMAGES
        else:
            module.images_or_objects.value = M.M_IMAGES_AND_OBJECTS
            module.object_groups[0].object_name.value = OBJECTS_NAME
            object_set.add_objects(objects, OBJECTS_NAME)
        pipeline = cpp.Pipeline()
        workspace = cpw.Workspace(pipeline,
                                  module,
                                  image_set,
                                  object_set,
                                  cpmeas.Measurements(),
                                  image_set_list)
        return workspace, module

    def test_01_01_load_matlab(self):
        '''Load a Matlab pipeline with a MeasureCorrelation module'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0'
                'sSU1RyM+zUgjJKFXwKs1TMDRUMLC0MjS1MjZTMDIwsFQgGTAwevryMzAwSD'
                'EzMFTMeRtxN++WgYiZQMT10NjrWZeWFB58qhfBfre/bGefn/Qlroy1Wr63j'
                'voYXJmcvPjIyoT8zbttj8ml92+UEOLQSzjO0rYsctOaxz9qns95f+O45zdG'
                'hr/HGUSaCtVfRBrk/Qw4d2TXBH2B5zO+7bHZcGBxwb/wC+sXdCfOXqDtUfO'
                'k0bP72estp/Xa/55cXHztI2eWg/o+iwze+5nK17PLlI9+KOTmF9h54L7gjN'
                'yLm/xfsFXPuBhgf2R6unqZ5PQ379hrC+pPObs9Osj1KzAnbk0987LXay33y'
                'B65Jt/yV4j3x+Vy5ozPk5h31uoWaHHNucPjxzfH1M/9W7z2F65Jfw91xM9W'
                'sPlWH1tWfmBNrOL1dYpLO+Ysebjdy17/JffONg5Byesnb8d6xp/Yqphey2S'
                'rPie+1X7qPNPF6Y3hT8VFZfe/96zj3vl0k90bRzmZps77WnNiOd1PpK9xkd'
                'T/KTfr2P5DditmffhuabF5WdlsvXd7eb2CZ31cXXDplvtNyTk6GQa2vz9/c'
                '55cXffSNjHXQ+2b77ngu422S042681f9ttx6fSZF083rEq7s8pqStgdLZm7'
                'NmpP1wety1syb9nU/66VPlH+2senvlL7vH3dX/mn+pl/V4T9y7s3L/uV7qn'
                'ZjfdO557ZzpV+72/gcplA/s+KHvfnZ/xZcKBa4SGn5GW+fQdl5ScJiYU3ix'
                '/21va7XF0UWiv837/2XJN4Tc7xN6eTLxUX72Gab/VvxoNvMRZfcjwCeI5/k'
                'fM/dV5JJlTG83zzOvtlv9Nj/534cyHd4OqfNae6ez5/Pvfp/fuKu56b8p9/'
                'tNYKsp3+s7Z2TuX7xDV/eW/WcE1ZZn8xI6g/uW5q062eX9lHvLXjRM/t+a8'
                'ZPGdjtFqpbqadmez3bZ+XV+v5VPq8vvO3///9vni50NJ3AYdEjT5bHhS5q1'
                'Vy+s/9a4V3P9af1dm3/ul7g8tW3yce9LP95rhQ+LozMMS/8i2SKW/XFbf+W'
                'J54+bfBod0OZotlXxzbH+xTYe9+4XNsSPK67hNfyt+u/b66qel5joKs3Nu3'
                'y77aux6Pq9OfPvm/8sovawr+eW+M/BOoI976L39Cjr1t5Ca7rNu7/vE73Wj'
                '5BgDjormq')
        #
        # 4 modules, MeasureCorrelation is last
        #
        # Images:
        #    DNA
        #    Cytoplasm
        # Measure images and objects
        # Objects:
        #    Nuclei
        #    Cells
        #
        fd = StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cpp.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()),4)
        module = pipeline.modules()[-1]
        self.assertEqual(module.images_or_objects.value, M.M_IMAGES_AND_OBJECTS)
        self.assertEqual(module.image_count.value, 2)
        for name in [x.image_name.value for x in module.image_groups]:
            self.assertTrue(name in ["DNA","Cytoplasm"])
        
        self.assertEqual(module.object_count.value, 2)
        for name in [x.object_name.value for x in module.object_groups]:
            self.assertTrue(name in ["Nuclei","Cells"])
        
    def test_01_02_load_v1(self):
        '''Load a version-1 MeasureCorrelation module'''
        data = ('eJztW++O2kYQXzju2muk6FKpatR82Y+59kCG5NoLqi5Q6B/ag6AcTRRFabs'
                'HC2y17CJ7fTlaRcoj9RH6GH2Efswj1As2NlsfNmBzENmSBTPsb2ZndnZmbO'
                'N6uXVW/gYe5zRYL7eyXUIxbFIkulwfFCETR7CiYyRwB3JWhK2+CX80Gczno'
                'XZSfHBc1AqwoGmPwHJHqla/bX30TwDYsz4/tM60/dOuTac8p6TPsRCE9Yxd'
                'kAF3bf7f1vkM6QRdUPwMURMbrgqHX2Nd3hoNpz/VecekuIEG3sHW0TAHF1g'
                '3nnQdoP1zk1xhek7+wIoJzrCn+JIYhDMbb8tXuVO9XCh6pR/++sz1Q0rxQ8'
                'Y673n4cvwPwB2f8fHbHc/4A5smrEMuScdEFJIB6k1nIeVpAfJ2ZuTtgGqjP'
                'MadBOD2lHnsjf3cppiE05uawadAwZ5vKQB3oOiVZwtfiey3V6gt4ACJdj+K'
                '+QfhdxW8pCuYUiOk36+zf1Hcg5C4zAwuA748eqiF8fctxU5JN3U+RD0krE0'
                'w5scZZ35+rp2d/VxfUu8La3eEsXtf0SvpykjwIUXGwOZHKSfIjvSMnDRo8N'
                'VwQfP2W/cnwjDh95RfIDqdd1C++liRI+naOElBxKwCdPE7bgsDhJb3qSJP0'
                'lXcRSYVcCwXVoluieT6aKX4WBSXz2mR5809Be8cDn4fuH4rBeiNaj396o+W'
                '08bHUd7+4plX3Hk06vVbNI9atudXWbdl7Yt6nRbNI3lttXgNigtvv3Rg05U'
                '+YgzTQlTrFBJ3vM71depiKQDnV1dqTGBmEDHy6A+S85EiR9JVDhkX0DSwvx'
                '1R2q/2M/mQ8w5r/6L+13zyQJT2qvHV4AxHtf+W1beIfW8D9P0EZtdF0r/cf'
                '9z8Wl6A4tPcF4e/Suq5leKf8tenL8vZ5qtDh1Ph1Byw05da9tGrP/NHhTeT'
                'wefEQo6Zh6H9rMbVVyFxYfqsRfzVD9B3ovhL0tLmFxjptiMevjnMSladM9G'
                '3eQWbV0UjlxNnP+zXP7Rec9i2+ljDvuK8oXqQjzLPLVNXn2PS68vbKZfyxg'
                'FrO/cT4uznorquWDYe/Pz5HddxT+cm66xuf1zXz2H6xWXnuQl1YlPsexswz'
                '02pE3HW/22uE1H3DZu2v6Ku85tm36bkgXXZp+WOb3yecd+vibLfWjduU/qq'
                'TVvndfZRi+D+ueviUgrO77nVOv0zfsglHTQML8dvP01uPruCtmVfeOYNCev'
                'gYYzytmWf3XT8beu8t9X+BBddX7EJeTCxN8EluOtxJTA/zg/AbJzL083Tk7'
                'IeZ5/i95yfm4IShv/XWGyT3993XAnMX9ek/ie4OHDbnk9KAfOPOx8nuASX4'
                'FbHlTy4pP4luASX4BLc+497l3Jx6vMNSXuff8vxv3n0+NWJz8FsnZB0G1M6'
                '1Ll8/0rPDcYvCRk5ylFn8pZO7sz6WvO8sCP1DAP0lBQ9pev0kA5mgnRHQ93'
                'SZgo+QIK0czWb27S4ZYcr9fYD9Pr9/2CuXgO3OesgfTTVee5wwthZVPQVr9'
                'M3wMgwdUu0rmM6ficlV5+wKi7L9a83XvZ99HrXPW1Rn9y788G8OANgNr7cu'
                'Hv3eBl96Z106jaY/T/crQBcBszGu8T/CxaL7/tzxjs2bur4/wDdHk0H')
        #
        # 4 modules, MeasureCorrelation is last
        #
        # Images:
        #    DNA
        #    Cytoplasm
        # Measure images and objects
        # Objects:
        #    Nuclei
        #    Cells
        #
        fd = StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cpp.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()),4)
        module = pipeline.modules()[-1]
        self.assertEqual(module.images_or_objects.value, M.M_IMAGES_AND_OBJECTS)
        self.assertEqual(module.image_count.value, 2)
        for name in [x.image_name.value for x in module.image_groups]:
            self.assertTrue(name in ["DNA","Cytoplasm"])
        
        self.assertEqual(module.object_count.value, 2)
        for name in [x.object_name.value for x in module.object_groups]:
            self.assertTrue(name in ["Nuclei","Cells"])
        
    def test_02_01_get_categories(self):
        '''Test the get_categories function for some different cases'''
        module = M.MeasureCorrelation()
        module.image_groups[0].image_name.value = IMAGE1_NAME
        module.image_groups[1].image_name.value = IMAGE2_NAME
        module.object_groups[0].object_name.value = OBJECTS_NAME
        module.images_or_objects = M.M_IMAGES
        def cat(name):
            return module.get_categories(None, name) == ["Correlation"]
        self.assertTrue(cat("Image"))
        self.assertFalse(cat(OBJECTS_NAME))
        module.images_or_objects = M.M_OBJECTS
        self.assertFalse(cat("Image"))
        self.assertTrue(cat(OBJECTS_NAME))
        module.images_or_objects = M.M_IMAGES_AND_OBJECTS
        self.assertTrue(cat("Image"))
        self.assertTrue(cat(OBJECTS_NAME))
    
    def test_02_02_get_measurements(self):
        '''Test the get_measurements function for some different cases'''
        module = M.MeasureCorrelation()
        module.image_groups[0].image_name.value = IMAGE1_NAME
        module.image_groups[1].image_name.value = IMAGE2_NAME
        module.object_groups[0].object_name.value = OBJECTS_NAME
        module.images_or_objects = M.M_IMAGES
        def meas(name):
            if name == "Image":
                ans = list(module.get_measurements(None,name,"Correlation"))
                ans.sort()
                return ans == ["Correlation", "Slope"]
            return module.get_measurements(None, name, "Correlation") == ["Correlation"]
        self.assertTrue(meas("Image"))
        self.assertFalse(meas(OBJECTS_NAME))
        module.images_or_objects = M.M_OBJECTS
        self.assertFalse(meas("Image"))
        self.assertTrue(meas(OBJECTS_NAME))
        module.images_or_objects = M.M_IMAGES_AND_OBJECTS
        self.assertTrue(meas("Image"))
        self.assertTrue(meas(OBJECTS_NAME))
    
    def test_02_03_get_measurement_images(self):
        '''Test the get_measurment_images function for some different cases'''
        module = M.MeasureCorrelation()
        module.image_groups[0].image_name.value = IMAGE1_NAME
        module.image_groups[1].image_name.value = IMAGE2_NAME
        module.object_groups[0].object_name.value = OBJECTS_NAME
        module.images_or_objects = M.M_IMAGES
        def meas(name):
            ans = module.get_measurement_images(None, name, "Correlation",
                                                "Correlation")
            if len(ans) == 0:
                return False
            self.assertTrue(ans[0] in ["%s_%s"% x for x in ((IMAGE1_NAME,IMAGE2_NAME),
                                                            (IMAGE2_NAME,IMAGE1_NAME))])
            return True
        self.assertTrue(meas("Image"))
        self.assertFalse(meas(OBJECTS_NAME))
        module.images_or_objects = M.M_OBJECTS
        self.assertFalse(meas("Image"))
        self.assertTrue(meas(OBJECTS_NAME))
        module.images_or_objects = M.M_IMAGES_AND_OBJECTS
        self.assertTrue(meas("Image"))
        self.assertTrue(meas(OBJECTS_NAME))
        
    def test_03_01_correlated(self):
        np.random.seed(0)
        image = np.random.uniform(size = (10,10))
        i1 = cpi.Image(image)
        i2 = cpi.Image(image)
        workspace, module = self.make_workspace(i1, i2)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,cpmeas.IMAGE, "Correlation","Correlation")
        corr = m.get_current_measurement(cpmeas.IMAGE, "Correlation_Correlation_%s"%mi[0])
        self.assertAlmostEqual(corr,1)
    
    def test_03_02_anticorrelated(self):
        '''Test two anticorrelated images'''
        #
        # Make a checkerboard pattern and reverse it for one image
        #
        i,j = np.mgrid[0:10,0:10]
        image1 = ((i+j)%2).astype(float)
        image2 = 1-image1
        i1 = cpi.Image(image1)
        i2 = cpi.Image(image2)
        workspace, module = self.make_workspace(i1, i2)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,cpmeas.IMAGE, "Correlation","Correlation")
        corr = m.get_current_measurement(cpmeas.IMAGE, "Correlation_Correlation_%s"%mi[0])
        self.assertAlmostEqual(corr,-1)
    
    def test_04_01_slope(self):
        '''Test the slope measurement'''
        np.random.seed(0)
        image1 = np.random.uniform(size = (10,10))
        image2 = image1 * .5
        i1 = cpi.Image(image1)
        i2 = cpi.Image(image2)
        workspace, module = self.make_workspace(i1, i2)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,cpmeas.IMAGE, "Correlation","Slope")
        slope = m.get_current_measurement(cpmeas.IMAGE, "Correlation_Slope_%s"%mi[0])
        if mi[0] == "%s_%s"%(IMAGE1_NAME,IMAGE2_NAME):
            self.assertAlmostEqual(slope, .5)
        else:
            self.assertAlmostEqual(slope, 2)
            
    def test_05_01_crop(self):
        '''Test similarly cropping one image to another'''
        np.random.seed(0)
        image1 = np.random.uniform(size = (20,20))
        i1 = cpi.Image(image1)
        crop_mask = np.zeros((20,20),bool)
        crop_mask[5:16,5:16] = True
        i2 = cpi.Image(image1[5:16,5:16],crop_mask = crop_mask)
        workspace, module = self.make_workspace(i1, i2)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,cpmeas.IMAGE, "Correlation","Correlation")
        corr = m.get_current_measurement(cpmeas.IMAGE, "Correlation_Correlation_%s"%mi[0])
        self.assertAlmostEqual(corr,1)
    
    def test_05_02_mask(self):
        '''Test images with two different masks'''
        np.random.seed(0)
        image1 = np.random.uniform(size = (20,20))
        mask1 = np.ones((20,20),bool)
        mask1[5:8,8:12] = False
        mask2 = np.ones((20,20),bool)
        mask2[14:18,2:5] = False
        mask = mask1 & mask2
        image2 = image1.copy()
        #
        # Try to confound the module by making masked points anti-correlated
        #
        image2[~mask] = 1-image1[~mask]
        i1 = cpi.Image(image1, mask=mask1)
        i2 = cpi.Image(image2, mask=mask2)
        workspace, module = self.make_workspace(i1, i2)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,cpmeas.IMAGE, "Correlation","Correlation")
        corr = m.get_current_measurement(cpmeas.IMAGE, "Correlation_Correlation_%s"%mi[0])
        self.assertAlmostEqual(corr,1)
    
    def test_06_01_objects(self):
        '''Test images with two objects'''
        labels = np.zeros((10,10), int)
        labels[:4,:4] = 1
        labels[6:,6:] = 2
        i,j = np.mgrid[0:10,0:10]
        image1 = ((i+j)%2).astype(float)
        image2 = image1.copy()
        #
        # Anti-correlate the second object
        #
        image2[labels==2] = 1-image1[labels==2]
        i1 = cpi.Image(image1)
        i2 = cpi.Image(image2)
        o  = cpo.Objects()
        o.segmented = labels
        workspace, module = self.make_workspace(i1, i2, o)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,OBJECTS_NAME, 
                                           "Correlation","Correlation")
        corr = m.get_current_measurement(OBJECTS_NAME, "Correlation_Correlation_%s"%mi[0])
        self.assertEqual(len(corr), 2)
        self.assertAlmostEqual(corr[0],1)
        self.assertAlmostEqual(corr[1],-1)
        
    def test_06_02_cropped_objects(self):
        '''Test images and objects with a cropping mask'''
        np.random.seed(0)
        image1 = np.random.uniform(size = (20,20))
        i1 = cpi.Image(image1)
        crop_mask = np.zeros((20,20),bool)
        crop_mask[5:15,5:15] = True
        i2 = cpi.Image(image1[5:15,5:15],crop_mask = crop_mask)
        labels = np.zeros((10,10), int)
        labels[:4,:4] = 1
        labels[6:,6:] = 2
        o  = cpo.Objects()
        o.segmented = labels
        #
        # Make the objects have the cropped image as a parent
        #
        o.parent_image = i2
        workspace, module = self.make_workspace(i1, i2,o)
        module.run(workspace)
        m = workspace.measurements
        mi = module.get_measurement_images(None,OBJECTS_NAME, "Correlation","Correlation")
        corr = m.get_current_measurement(OBJECTS_NAME, "Correlation_Correlation_%s"%mi[0])
        self.assertAlmostEqual(corr[0],1)
        self.assertAlmostEqual(corr[1],1)
        