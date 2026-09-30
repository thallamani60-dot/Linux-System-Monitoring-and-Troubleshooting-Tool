# Disk usage rise (bounded simulation)

**Symptom:** filesystem usage crosses threshold. Use `TEST_DIR=$(mktemp -d /tmp/sentinel-disk.XXXXXX)` then `fallocate -l 64M "$TEST_DIR/sample.bin"` (or `dd if=/dev/zero of="$TEST_DIR/sample.bin" bs=1M count=64 status=progress` where fallocate is unavailable). Check `df -h /` and `du -sh "$TEST_DIR"`; reduce the test size if free space is limited. Remove only the named file and directory with `rm -- "$TEST_DIR/sample.bin" && rmdir -- "$TEST_DIR"`. Verify `df -h /` returns near its prior reading. Never target arbitrary paths or fill the filesystem.
