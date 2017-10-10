'''

 All components of this library are licensed under the BSD 3-Clause
 License.

 Copyright (c) 2015-, Algorithmic Robotics and Control Group @Rutgers
 (http://arc.cs.rutgers.edu). All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are
 met:

 Redistributions of source code must retain the above copyright notice,
 this list of conditions and the following disclaimer.  Redistributions
 in binary form must reproduce the above copyright notice, this list of
 conditions and the following disclaimer in the documentation and/or
 other materials provided with the distribution. Neither the name of
 Rutgers University nor the names of the contributors may be used to
 endorse or promote products derived from this software without specific
 prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
"""
All cars goes in a single big circle. 

"""

import math

def GetPath(num, bound):
    paths = [list() for x in range(num)]

    radius = bound.height / 2
    center = ((bound.l + bound.r) / 2, (bound.u + bound.d) / 2)
    step1 = 2 * math.pi / num
    step2 = 2 * math.pi / 50
    print radius, center, step1, step2
    for j in range(num):
        angle = j * step1
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        paths[j].append((x, y))
        for i in range(150):
            angle += step2
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            paths[j].append((x, y))
    return paths