#coding=utf-8
import sys
sys.path.append("C:/cgteamwork/bin/base/ct_plu/")
sys.path.append("c:/cgteamwork/bin/base/")

from cgtw2 import *
import ct_plu

class ct_base(ct_plu.extend):
    @classmethod
    def set_flow(cls, t, data, module, info):
        t.task.update_flow(data, module, info[0], 'task.tjdqr', 'Retake')
        #t.task.set(data, module, info[0], {'task.tjdqr': 'Retake'})#修改无效果
        t.client.refresh_id(data, module, 'task', info)

    def __init__(self):
        ct_plu.extend.__init__(self)  #继承

    def run(self, a_dict_data):
        try:
            t_tw = tw()
            t_argv = ct_plu.argv(a_dict_data)
            data = t_argv.get_sys_database()
            module = t_argv.get_sys_module()

            cache_id_lis = t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and', ["pipeline.entity", "=", "Ani_Cache"]])
            fx_id_lis = t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and', ["pipeline.entity", "=", "Fx"]])
            render_id_lis = t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and', ["pipeline.entity", "=", "Render"]])

            filebox_id = t_argv.get_sys_id()[0]  #获取拖入文件筐操作所在项的id
            shot_info = t_tw.task.get_field_and_dir('proj_xxtt', 'shot', [filebox_id], ['shot.entity'], ['render_final']
                                                    )[0]['shot.entity']#镜头号
            print(shot_info)
            if filebox_id in cache_id_lis or filebox_id in fx_id_lis:
                if filebox_id in cache_id_lis:
                    print('Ani_Cache')
                else:
                    print('FX')
                self.set_flow(t_tw, data, module, t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and',
                                                                                          ["pipeline.entity", "=", "Render"], 'and',
                                                                                          ['shot.entity', '=', shot_info]]))
                self.set_flow(t_tw, data, module, t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and',
                                                                                           ["pipeline.entity", "=", "Cmp"], 'and',
                                                                                           ['shot.entity', '=', shot_info]]))
            elif filebox_id in render_id_lis:
                print('Render')
                self.set_flow(t_tw, data, module, t_tw.task.get_id(data, module, [["eps.entity", "=", "ceshi"], 'and',
                                                                                           ["pipeline.entity", "=", "Cmp"], 'and',
                                                                                           ['shot.entity', '=', shot_info]]))
            else:
                self.ct_false(u'没有找到与当前文件筐所在项对应[Ani_Cache、Fx、Render]的id')
        except:
            from traceback import format_exc
            self.ct_false(format_exc())


if __name__ == "__main__":
    t_debug_argv_dict = ct_plu.argv().get_debug_argv_dict()
    print(ct_base().run(t_debug_argv_dict))

