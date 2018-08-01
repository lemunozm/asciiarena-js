package main

import "hash/crc64"
import "math/rand"

type Map struct {
	width  uint
	height uint
	seed   string
}

func NewMap(width uint, height uint, seed string) *Map {
	m := &Map{
		width:  width,
		height: height,
		seed:   seed,
	}

	crc64.Checksum([]byte(seed), crc64.MakeTable(crc64.ECMA))
	//TODO (generate map)
	return m
}

func (m Map) Width() uint {
	return m.width
}

func (m Map) Height() uint {
	return m.height
}

func (m Map) Seed() string {
	return m.seed
}

func (m *Map) ComputePlayerOrigins(players []uint8, rand *rand.Rand) {
	//TODO
}
