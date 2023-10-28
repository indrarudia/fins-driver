import unittest

from fins.memory import MemoryArea, MemoryAreaCode


class MemoryAreaTest(unittest.TestCase):
    def test_memory_area_word(self) -> None:
        cio = MemoryArea("CIO100")
        self.assertEqual(cio.raw, MemoryAreaCode.CIO_WORD + b"\x00\x64\x00")

        work = MemoryArea("W100")
        self.assertEqual(work.raw, MemoryAreaCode.WORK_WORD + b"\x00\x64\x00")

        holding = MemoryArea("H100")
        self.assertEqual(holding.raw, MemoryAreaCode.HOLDING_WORD + b"\x00\x64\x00")

        auxiliary = MemoryArea("A100")
        self.assertEqual(auxiliary.raw, MemoryAreaCode.AUXILIARY_WORD + b"\x00\x64\x00")

        dm = MemoryArea("D100")
        self.assertEqual(dm.raw, MemoryAreaCode.DATA_MEMORY_WORD + b"\x00\x64\x00")

    def test_memory_area_bit(self) -> None:
        cio = MemoryArea("CIO100.01")
        self.assertEqual(cio.raw, MemoryAreaCode.CIO_BIT + b"\x00\x64\x01")

        work = MemoryArea("W100.01")
        self.assertEqual(work.raw, MemoryAreaCode.WORK_BIT + b"\x00\x64\x01")

        holding = MemoryArea("H100.01")
        self.assertEqual(holding.raw, MemoryAreaCode.HOLDING_BIT + b"\x00\x64\x01")

        auxiliary = MemoryArea("A100.01")
        self.assertEqual(auxiliary.raw, MemoryAreaCode.AUXILIARY_BIT + b"\x00\x64\x01")

        dm = MemoryArea("D100.01")
        self.assertEqual(dm.raw, MemoryAreaCode.DATA_MEMORY_BIT + b"\x00\x64\x01")


if __name__ == "__main__":
    unittest.main()
