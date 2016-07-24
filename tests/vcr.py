import vcr


MOCK_RECORDING_ENABLED = False


vcr = vcr.VCR(
    cassette_library_dir='mock/',
    record_mode='once' if MOCK_RECORDING_ENABLED else 'none',
    match_on=['uri'],
)
