#!/usr/bin/env python
import base64
import os

from duckietown_utils import (DTUserError, DTConfigException, format_table_plus,
                              get_duckiefleet_root, indent, locate_files, memoize_simple, system_cmd_result,
                              write_data_to_file)
from duckietown_utils.cli import D8App, d8app_run
from easy_algo import get_easy_algo_db
from duckietown_utils.path_utils import expand_all


class CreateRoster(D8App):
    """ Creates the roster """
    def define_program_options(self, params):
        params.accept_extra() 
        g = 'People DB'
        params.add_string('roster', default=None, 
                          help="Write roster to this filename", group=g) 
        
    def go(self):
        
        db = get_easy_algo_db()
        
        extra = self.options.get_extra()
        if len(extra) > 1:
            msg = 'Only one extra param accepted.'
            raise DTUserError(msg)
        
        if len(extra) == 1:
            query = extra[0]
        else:
            query = 'all'
             
        persons = db.query_and_instance('person', query)
        
        if self.options.roster:
            out_file = expand_all(self.options.roster)
            outd = os.path.dirname(out_file)
            roster = create_roster(persons, outd)
            write_data_to_file(roster, out_file)
        else:
            # instance ll
            tags = set()
            for p in persons.values():
                tags.update(p.get_tags())
                
            print(list(persons))
            print('tags: %s' % list(tags))
            table = table_people(persons)
            print(table)

def table_people(people):
    table = []
    table.append(['ID', 'name', 'tags'])
    for idp, person in people.items():
        row = []
        row.append(idp)
        row.append(person.get_name())
        row.append(", ".join(person.get_tags()))
        table.append(row)
    s = ''
#     remove_table_field(table, 'filename')
    s += indent(format_table_plus(table, colspacing=4), '| ')
    return s

def create_roster(people, outd):
    
    s = ''
    S = '\n\n'
    s += '<div style="display:none" id="autogenerated-roster">'
    for k, person in people.items():
        jpg = get_image_for_person(k, 128)
        basename = k + '.small.jpg'
        jpg_file = os.path.join(outd, 'roster-images', basename)
        write_data_to_file(jpg, jpg_file)
        name = person.get_name()
        s += '<div id="%s-roster" class="roster-person">' % k 
        s += '\n <span class="name">%s</span>' % name 
        s += '\n <img src="%s"/>' % basename 
        s += '\n' + indent(roster_css, '  ')
        s += '\n</div>' + S + S
        
    s += S + '</div>'
    return s

nopic = 'MISSING.jpg'

def get_image_for_person(pid, size):
    basename2filename = get_images()
    b = '%s.jpg' % pid
    if not b in basename2filename:
        b = nopic
    tmp= 'tmp.jpg'
    cwd = '.'
    cmd = ['convert', basename2filename[b], '-resize', str(size), tmp]
    system_cmd_result(cwd, cmd,
                      display_stdout=False,
                      display_stderr=False,
                      raise_on_error=True) 
    jpg = open(tmp).read()
    return jpg
    
@memoize_simple
def get_images():
    found = locate_files(get_duckiefleet_root(), '*.jpg')
    basename2filename = dict((os.path.basename(_), _) for _ in found)
    if not nopic in basename2filename:
        msg = 'I expect a file %r to represent missing pictures.' % nopic
        raise DTConfigException(msg)
    return basename2filename
    
def inline_jpg(data):
    encoded = base64.b64encode(data)
    mime = 'image/jpg'
    link = 'data:%s;base64,%s' % (mime, encoded)
    return link

roster_css = """
<style>
div.roster-person {
    display: inline-block;
    width: 8em;
    height: 8em;
    text-align: center;
    float: left;
}
div.roster-person span.name {
    display: block;
}
div.roster-person img {
    max-width: 7em;
    max-height: 7em;
}
</style>
"""
    
if __name__ == '__main__':
    d8app_run(CreateRoster)
    