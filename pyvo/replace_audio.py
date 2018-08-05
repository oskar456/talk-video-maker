#!/usr/bin/env python3

from talk_video_maker import mainfunc, opts
from talk_video_maker.syncing import offset_video, get_audio_offset


@mainfunc(__name__)
def replace_audio(
        video: opts.VideoOption(
            default='*.mkv',
            help='Video file'),
        audio: opts.VideoOption(
            default='*.mp4',
            help='Audio file'),
        trim: opts.TextOption(
            default='a',
            help='Video trimming mode '
                 '(a=whole video, b=whole audio, '
                 'pad=include both, intersect=include only common part)'),
        preview: opts.FlagOption(
            help='Only process a small preview of the video'),
        offset: opts.FloatOption(
            default=None,
            help='Manual time offset of between recordings'),
        outpath: opts.PathOption(
            default='.',
            help='Path where to put the output file'),
        ):

    if not video:
        raise ValueError('No video')
    if not audio:
        raise ValueError('No audeo')

    if offset is None:
        if not any(s.type == 'audio' for s in video.streams):
            raise ValueError('video has no audio, specify offset manually')
        offset = get_audio_offset(video, audio, max_stderr=5e-4,
                                  max_speed_error=1e-2)

    video, audio = offset_video(video, audio, offset, mode=trim)
    video = video.muted()
    audio = audio.without_streams('video')
    main = video | audio
    if preview:
        main = main.trimmed(end=30)
    result = main

    print(result.graph)
    return result
