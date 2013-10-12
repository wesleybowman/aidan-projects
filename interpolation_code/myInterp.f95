subroutine linear(m,x,y,n,a,z)
      integer m,n
      real, intent(in) :: x(m)
      real, intent(in) :: y(m)
      real, intent(in) :: a(n)
      real, intent(out) :: z(n)

!      Uncomment if you do not want extrapolation
!      do i=1, n
!
!      if (a(i) .le. x(1) .or. a(i).ge.x(m)) then
!          write ( *, '(a)'    ) ' '
!          write ( *, '(a)'    ) '  You are trying to extrapolate'
!          write ( *, '(a)'    ) ' '
!          write ( *, '(a)'    ) '  Programming Stopping'
!          write ( *, '(a)'    ) ' '
!          stop
!      endif
!      enddo

      do i=1, n
      do j=1, m

      if ( (a(i) .ge. x(j) .and. a(i) .le. x(j+1)) .or. (a(i) .le. x(j) .and. a(i) .ge. x(j+1)) ) then

          z(i)=y(j) + (y(j+1) - y(j)) * (a(i) - x(j)) / (x(j+1) - x(j))

      endif
      enddo
      enddo

      return



end subroutine linear
